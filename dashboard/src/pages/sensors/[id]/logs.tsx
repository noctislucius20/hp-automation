import {
  mdiAlertCircle,
  mdiArrowLeftThick,
  mdiClose,
  mdiCloseThick,
  mdiPencil,
  mdiRaspberryPi,
  mdiRocketLaunch,
} from '@mdi/js'
import Head from 'next/head'
import { ReactElement, useEffect, useState } from 'react'
import BaseButton from '../../../components/BaseButton'
import BaseButtons from '../../../components/BaseButtons'
import BaseDivider from '../../../components/BaseDivider'
import CardBox from '../../../components/CardBox'
import LayoutAuthenticated from '../../../layouts/Authenticated'
import SectionMain from '../../../components/SectionMain'
import SectionTitleLineWithButton from '../../../components/SectionTitleLineWithButton'
import { flaskApiUrl, getPageTitle } from '../../../config'
import NotificationBar from '../../../components/NotificationBar'
import Spinner from 'react-spinner-material'
import axios from 'axios'
import { useRouter } from 'next/router'
import io from 'socket.io-client'

const SensorLogs = () => {
  const router = useRouter()
  const { id } = router.query
  const [logs, setLogs] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [status, setStatus] = useState({ error: null })
  const [notifVisible, setNotifVisible] = useState(true)
  const [isSpinnerVisible, setIsSpinnerVisible] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showStopButton, setShowStopButton] = useState(false)

  setTimeout(() => {
    setShowStopButton(true)
  }, 7000)

  useEffect(() => {
    let mounted = true
    const socket = io(
      process.env.NODE_ENV === 'production'
        ? 'http://192.168.195.195:8080'
        : 'http://localhost:5000',
      {
        rememberUpgrade: true,
      }
    )

    if (id) {
      const getLogs = async () => {
        try {
          socket.on('logs', (data) => {
            if (mounted) {
              setLogs((logs) => [...logs, data])
            }
          })

          const token = JSON.parse(localStorage.getItem('token'))
          const config = {
            method: 'GET',
            url: `${flaskApiUrl}/sensors/${id}/logs`,
            headers: {
              Authorization: `Bearer ${token.access_token}`,
            },
          }

          const response = await axios.request(config)

          setIsLoading(false)
          if (response.data.data || response.data.data == '') {
            setLogs((logs) => [...logs, response.data.data])
            setIsSpinnerVisible(false)
          }
        } catch (error) {
          console.log(error)
          setStatus({
            error: {
              message:
                error.response == undefined ? 'Something went wrong' : error.response.data.message,
              code: error.response == undefined ? 500 : error.response.status,
            },
          })
        }
      }

      getLogs()
    }

    return () => {
      mounted = false
      socket.disconnect()
    }
  }, [id, logs])

  useEffect(() => {
    setTimeout(() => {
      setNotifVisible(false)
    }, 60000)
  }, [notifVisible])

  const handleRelaunchJob = async () => {
    try {
      setIsSubmitting(true)
      const token = JSON.parse(localStorage.getItem('token'))
      const config = {
        method: 'POST',
        url: `${flaskApiUrl}/sensors/${id}/relaunch`,
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
      }

      await axios.request(config)

      router.push(`/sensors/${id}`)
    } catch (error) {
      console.log(error)
      setStatus({
        error: {
          message:
            error.response == undefined ? 'Something went wrong' : error.response.data.message,
          code: error.response == undefined ? 500 : error.response.status,
        },
      })

      router.push(`/sensors/${id}`)
    }
  }

  const handleCancelJob = async () => {
    try {
      setIsSubmitting(true)
      const token = JSON.parse(localStorage.getItem('token'))
      const config = {
        method: 'POST',
        url: `${flaskApiUrl}/sensors/${id}/cancel`,
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
      }

      await axios.request(config)

      router.push(`/sensors/${id}/logs`)
    } catch (error) {
      console.log(error)
      setStatus({
        error: {
          message:
            error.response == undefined ? 'Something went wrong' : error.response.data.message,
          code: error.response == undefined ? 500 : error.response.status,
        },
      })

      router.push(`/sensors/${id}`)
    }
  }

  return (
    <>
      <Head>
        <title>{getPageTitle(`Logs: `)}</title>
      </Head>

      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiRaspberryPi}
          title="Sensors"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiPencil} title={`Logs`}>
          <BaseButton
            href="/sensors/[id]"
            as={`/sensors/${id}`}
            icon={mdiArrowLeftThick}
            label="Back"
            color="danger"
            small
            roundedFull
            onClick={() => {
              io().disconnect()
            }}
          />
        </SectionTitleLineWithButton>

        {status && status.error && notifVisible && (
          <NotificationBar
            color="danger"
            icon={mdiAlertCircle}
            button={
              <BaseButton
                color="white"
                roundedFull
                small
                icon={mdiClose}
                onClick={() => {
                  setStatus({ error: null })
                }}
              />
            }
          >
            Error {status.error.code}: {status.error.message}
          </NotificationBar>
        )}
        <CardBox>
          {isLoading ? (
            <div className="h-96">Generating Logs...</div>
          ) : (
            <div
              className="overflow-auto text-overflow-ellipsis h-96 rounded-lg "
              dangerouslySetInnerHTML={{
                __html: logs.at(-1),
              }}
            ></div>
          )}
          <BaseDivider />
          <BaseButtons type="justify-between">
            {isSpinnerVisible ? (
              <>
                {showStopButton ? (
                  <BaseButton
                    type="button"
                    color="danger"
                    label="Stop"
                    disabled={!isSpinnerVisible}
                    icon={mdiCloseThick}
                    onClick={handleCancelJob}
                  />
                ) : (
                  <div></div>
                )}

                <Spinner radius={25} color={'#fff'} stroke={2} visible={true} />
              </>
            ) : (
              <BaseButton
                type="button"
                color="info"
                label="Relaunch"
                icon={mdiRocketLaunch}
                onClick={handleRelaunchJob}
                disabled={isSubmitting}
              />
            )}
          </BaseButtons>
        </CardBox>
      </SectionMain>
    </>
  )
}

SensorLogs.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default SensorLogs
