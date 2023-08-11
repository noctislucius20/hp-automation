import {
  mdiAlertCircle,
  mdiBeehiveOutline,
  mdiChartTimelineVariant,
  mdiClose,
  mdiFormatListCheckbox,
  mdiMonitorMultiple,
  mdiTable,
} from '@mdi/js'
import Head from 'next/head'
import React, { useEffect, useState } from 'react'
import type { ReactElement } from 'react'
import LayoutAuthenticated from '../layouts/Authenticated'
import SectionMain from '../components/SectionMain'
import SectionTitleLineWithButton from '../components/SectionTitleLineWithButton'
import CardBoxWidget from '../components/CardBoxWidget'
import CardBox from '../components/CardBox'
import { flaskApiUrl, getPageTitle } from '../config'
import axios from 'axios'
import TableDeployHistory from '../components/TableDeployHistory/TableDeployHistory'
import NotificationBar from '../components/NotificationBar'
import BaseButton from '../components/BaseButton'

const Dashboard = () => {
  const [deployHistory, setDeployHistory] = useState([])
  const [honeypots, setHoneypots] = useState([])
  const [sensors, setSensors] = useState([])
  const [status, setStatus] = useState({ error: null })
  const [isLoading, setIsLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(0)

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
        const token = JSON.parse(localStorage.getItem('token'))

        const config = {
          method: 'GET',
          url: `${flaskApiUrl}/sensors`,
          headers: { Authorization: `Bearer ${token.access_token}` },
        }
        const response = await axios.request(config)
        const distinctResponse = distinctArray(response.data.data)

        setSensors(distinctResponse)
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

    getSensors()
  }, [])

  useEffect(() => {
    const getHoneypots = async () => {
      try {
        const token = JSON.parse(localStorage.getItem('token'))

        const config = {
          headers: {
            Authorization: `Bearer ${token.access_token}`,
          },
          method: 'GET',
          url: `${flaskApiUrl}/honeypots`,
        }

        const response = await axios.request(config)
        setHoneypots(response.data.data)
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

    getHoneypots()
  }, [])

  useEffect(() => {
    const getDeployHistory = async () => {
      try {
        const token = JSON.parse(localStorage.getItem('token'))

        const config = {
          method: 'GET',
          url: `${flaskApiUrl}/sensors`,
          headers: {
            Authorization: `Bearer ${token.access_token}`,
          },
        }

        const response = await axios.request(config)

        setDeployHistory(response.data.data)
        setIsLoading(false)
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

    getDeployHistory()
  }, [])

  const handleResetStatus = () => {
    setStatus({ error: null })
  }

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  return (
    <>
      <Head>
        <title>{getPageTitle('Dashboard')}</title>
      </Head>
      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiChartTimelineVariant}
          title="Overview"
          main
        ></SectionTitleLineWithButton>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
          <CardBoxWidget
            icon={mdiMonitorMultiple}
            iconColor="warning"
            number={isLoading ? 0 : sensors.length}
            label="Total Sensors"
          />
          <CardBoxWidget
            icon={mdiBeehiveOutline}
            iconColor="success"
            number={isLoading ? 0 : honeypots.length}
            label="Total Honeypots"
          />
          <CardBoxWidget
            icon={mdiFormatListCheckbox}
            iconColor="info"
            number={isLoading ? 0 : deployHistory.length}
            label="Deployments Executed"
          />
        </div>

        <SectionTitleLineWithButton
          icon={mdiTable}
          title="Recent Deployment"
        ></SectionTitleLineWithButton>

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
            <TableDeployHistory
              deployHistory={deployHistory}
              status={status}
              currentPage={currentPage}
              pageChange={handlePageChange}
            />
          )}
        </CardBox>
      </SectionMain>
    </>
  )
}

Dashboard.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default Dashboard
