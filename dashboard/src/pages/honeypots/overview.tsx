import { mdiAlertCircle, mdiBeehiveOutline, mdiClose, mdiPlusThick, mdiTable } from '@mdi/js'
import axios from 'axios'
import Head from 'next/head'
import { useRouter } from 'next/router'
import { ReactElement, useEffect, useState } from 'react'
import BaseButton from '../../components/BaseButton'
import CardBox from '../../components/CardBox'
import NotificationBar from '../../components/NotificationBar'
import SectionMain from '../../components/SectionMain'
import SectionTitleLineWithButton from '../../components/SectionTitleLineWithButton'
import TableHoneypots from '../../components/TableHoneypot/TableHoneypots'
import { flaskApiUrl, getPageTitle } from '../../config'
import LayoutAuthenticated from '../../layouts/Authenticated'
import jwt from 'jsonwebtoken'

const HoneypotsPage = () => {
  const router = useRouter()
  const [honeypots, setHoneypots] = useState([])
  const [status, setStatus] = useState({ error: null })
  const [isLoading, setIsLoading] = useState(true)
  const [id, setId] = useState('')
  const [currentPage, setCurrentPage] = useState(0)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isModalTrashActive, setIsModalTrashActive] = useState(false)

  useEffect(() => {
    const checkIfNotAdmin = () => {
      const token = JSON.parse(localStorage.getItem('token'))
      const user = jwt.decode(token.access_token)
      if (!user.roles.includes('admin')) {
        router.push('/errors/forbidden')
      }
    }
    checkIfNotAdmin()
  }, [router])

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

    getHoneypots()
  }, [])

  const handleModalConfirm = async () => {
    try {
      const token = JSON.parse(localStorage.getItem('token'))

      setIsSubmitting(true)
      const config = {
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
        method: 'DELETE',
        url: `${flaskApiUrl}/honeypots/${id}`,
      }

      await axios.request(config)
      setHoneypots(honeypots.filter((honeypot) => honeypot.id !== id))
      setIsModalTrashActive(false)
      setId('')
    } catch (error) {
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
        <title>{getPageTitle('Honeypots')}</title>
      </Head>
      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiBeehiveOutline}
          title="Honeypots"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiTable} title="Overview">
          <BaseButton
            href="/honeypots/add"
            icon={mdiPlusThick}
            label="Add Honeypot"
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
            <TableHoneypots
              isSubmitting={isSubmitting}
              currentPage={currentPage}
              honeypots={honeypots}
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

HoneypotsPage.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default HoneypotsPage
