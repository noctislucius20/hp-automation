import {
  mdiAlertCircle,
  mdiChartTimelineVariant,
  mdiClose,
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
import jwt from 'jsonwebtoken'
import TableDeployHistory from '../components/TableDeployHistory/TableDeployHistory'
import NotificationBar from '../components/NotificationBar'
import BaseButton from '../components/BaseButton'

const Dashboard = () => {
  const [deployHistory, setDeployHistory] = useState([])
  const [status, setStatus] = useState({ error: null })
  const [isLoading, setIsLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(0)

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

  useEffect(() => {
    const getDeployHistory = async () => {
      try {
        if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
          await refreshJwtToken()
        }

        const token = JSON.parse(localStorage.getItem('token'))

        const config = {
          method: 'GET',
          url: `${flaskApiUrl}/sensors`,
          headers: {
            Authorization: `Bearer ${token.access_token}`,
          },
        }

        const response = await axios.request(config)
        // const distinctResponse = distinctArray(response.data.data)

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
            number={10}
            label="Total Host"
          />
          <CardBoxWidget
            icon={mdiMonitorMultiple}
            iconColor="success"
            number={5}
            label="Host Active"
          />
          <CardBoxWidget
            icon={mdiMonitorMultiple}
            iconColor="danger"
            number={5}
            label="Host Inactive"
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
        {/* <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="flex flex-col justify-between">
            {transactions.map((transaction: Transaction) => (
              <CardBoxTransaction key={transaction.id} transaction={transaction} />
            ))}
          </div>
          <div className="flex flex-col justify-between">
            {clientsListed.map((client: Client) => (
              <CardBoxClient key={client.id} client={client} />
            ))}
          </div>
        </div> */}

        {/* <SectionTitleLineWithButton icon={mdiChartPie} title="Trends overview">
          <BaseButton icon={mdiReload} color="whiteDark" onClick={fillChartData} />
        </SectionTitleLineWithButton>

        <CardBox className="mb-6">{chartData && <ChartLineSample data={chartData} />}</CardBox>

        <SectionTitleLineWithButton icon={mdiAccountMultiple} title="Clients" />

        <NotificationBar color="info" icon={mdiMonitorCellphone}>
          <b>Responsive table.</b> Collapses on mobile
        </NotificationBar>

        <CardBox hasTable>
          <TableSampleClients />
        </CardBox> */}
      </SectionMain>
    </>
  )
}

Dashboard.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default Dashboard
