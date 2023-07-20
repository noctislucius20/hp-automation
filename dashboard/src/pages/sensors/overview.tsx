import { mdiAlertCircle, mdiClose, mdiPlusThick, mdiRaspberryPi, mdiTable } from '@mdi/js'
import axios from 'axios'
import Head from 'next/head'
import { ReactElement, useEffect, useState } from 'react'
import BaseButton from '../../components/BaseButton'
import CardBox from '../../components/CardBox'
import SectionMain from '../../components/SectionMain'
import SectionTitleLineWithButton from '../../components/SectionTitleLineWithButton'
import TableSensors from '../../components/TableSensor/TableSensors'
import { flaskApiUrl, getPageTitle } from '../../config'
import jwt from 'jsonwebtoken'
import LayoutAuthenticated from '../../layouts/Authenticated'
import NotificationBar from '../../components/NotificationBar'

const SensorsPage = () => {
  const [sensors, setSensors] = useState([])
  const [status, setStatus] = useState({ error: null })
  const [isLoading, setIsLoading] = useState(true)
  const [id, setId] = useState('')
  const [currentPage, setCurrentPage] = useState(0)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isModalTrashActive, setIsModalTrashActive] = useState(false)

  const refreshJwtToken = async () => {
    try {
      const token = JSON.parse(localStorage.getItem('token'))
      const config = {
        method: 'PUT',
        url: `${flaskApiUrl}/auth`,
        data: { refresh_token: token.refresh_token },
      }
      const response = await axios.request(config)
      const accessToken = jwt.decode(response.data.data)

      localStorage.setItem('expirationTime', JSON.stringify(accessToken.exp))
      localStorage.setItem(
        'token',
        JSON.stringify({ access_token: response.data.data, refresh_token: token.refresh_token })
      )
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

  const distinctArray = (array) => {
    const newArray = array.map((item) =>
      JSON.stringify({
        id: item.id,
        ip_address: item.ip_address,
        name: item.name,
        created_at: item.created_at,
      })
    )
    const distinctSet = new Set<string>(newArray)
    const distinctArray = Array.from(distinctSet)
    const finalArray = distinctArray.map((item) => JSON.parse(item))
    return finalArray
  }

  useEffect(() => {
    const getSensors = async () => {
      try {
        if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
          await refreshJwtToken()
        }

        const token = JSON.parse(localStorage.getItem('token'))

        const config = {
          method: 'GET',
          url: `${flaskApiUrl}/sensors`,
          headers: { Authorization: `Bearer ${token.access_token}` },
        }
        const response = await axios.request(config)
        const distinctResponse = distinctArray(response.data.data)

        setSensors(distinctResponse)
        setIsLoading(false)
      } catch (error) {
        console.log(error)
        setIsLoading
        setStatus({
          error: {
            message:
              error.response == undefined ? 'Something went wrong' : error.response.data.message,
            code: error.response == undefined ? 500 : error.response.status,
          },
        })
      }
    }

    getSensors()
  }, [])

  const handleModalConfirm = async () => {
    try {
      if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
        await refreshJwtToken()
      }

      const token = JSON.parse(localStorage.getItem('token'))

      setIsSubmitting(true)
      const config = {
        method: 'DELETE',
        url: `${flaskApiUrl}/sensors/${id}`,
        headers: { Authorization: `Bearer ${token.access_token}` },
      }
      await axios.request(config)
      setSensors(sensors.filter((sensor) => sensor.id !== id))
      setIsModalTrashActive(false)
      setId('')
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

  const handleModalCancel = () => {
    setIsModalTrashActive(false)
    setId('')
  }

  const handleResetStatus = () => {
    setStatus({ error: null })
  }

  const handleModalDelete = (id) => {
    setIsModalTrashActive(true)
    setId(id)
  }

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  return (
    <>
      <Head>
        <title>{getPageTitle('Sensors')}</title>
      </Head>
      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiRaspberryPi}
          title="Sensors"
          main
        ></SectionTitleLineWithButton>
        <SectionTitleLineWithButton icon={mdiTable} title="Overview">
          <BaseButton
            href="/sensors/add"
            icon={mdiPlusThick}
            label="Add Sensor"
            color="success"
            small
            roundedFull
          />
        </SectionTitleLineWithButton>

        {status.error && (
          <NotificationBar
            color="danger"
            icon={mdiAlertCircle}
            button={
              <BaseButton
                color="white"
                roundedFull
                small
                icon={mdiClose}
                onClick={handleResetStatus}
              />
            }
          >
            Error {status.error.code}: {status.error.message}
          </NotificationBar>
        )}

        <CardBox className="mb-6" hasTable={!isLoading}>
          {isLoading ? (
            <div>Getting data...</div>
          ) : (
            <TableSensors
              isSubmitting={isSubmitting}
              currentPage={currentPage}
              sensors={sensors}
              id={id}
              isModalTrashActive={isModalTrashActive}
              modalCancel={handleModalCancel}
              modalConfirm={handleModalConfirm}
              modalDelete={handleModalDelete}
              pageChange={handlePageChange}
              status={status}
            />
          )}
        </CardBox>
      </SectionMain>
    </>
  )
}

SensorsPage.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default SensorsPage
