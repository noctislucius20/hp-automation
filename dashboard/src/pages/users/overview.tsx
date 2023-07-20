import { mdiAccountMultiple, mdiAlertCircle, mdiClose, mdiTable } from '@mdi/js'
import axios from 'axios'
import Head from 'next/head'
import { ReactElement, useEffect, useState } from 'react'
import BaseButton from '../../components/BaseButton'
import CardBox from '../../components/CardBox'
import NotificationBar from '../../components/NotificationBar'
import SectionMain from '../../components/SectionMain'
import SectionTitleLineWithButton from '../../components/SectionTitleLineWithButton'
import TableUsers from '../../components/TableUser/TableUsers'
import { flaskApiUrl, getPageTitle } from '../../config'
import LayoutAuthenticated from '../../layouts/Authenticated'
import jwt from 'jsonwebtoken'

const UsersPage = () => {
  const [users, setUsers] = useState([])
  const [status, setStatus] = useState({ error: null })
  const [isLoading, setIsLoading] = useState(true)
  const [id, setId] = useState('')
  const [currentPage, setCurrentPage] = useState(0)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isModalTrashActive, setIsModalTrashActive] = useState(false)
  const [currentUser, setCurrentUser] = useState('')

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
    const getUsers = async () => {
      try {
        if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
          await refreshJwtToken()
        }

        const token = JSON.parse(localStorage.getItem('token'))
        const accessToken = jwt.decode(token.access_token)
        setCurrentUser(accessToken.username)

        const config = {
          headers: {
            Authorization: `Bearer ${token.access_token}`,
          },
          method: 'GET',
          url: `${flaskApiUrl}/users`,
        }

        const response = await axios.request(config)
        setUsers(response.data.data)
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

    getUsers()
  }, [])

  const handleModalConfirm = async () => {
    try {
      if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
        await refreshJwtToken()
      }

      const token = JSON.parse(localStorage.getItem('token'))

      setIsSubmitting(true)
      const config = {
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
        method: 'DELETE',
        url: `${flaskApiUrl}/users/${id}`,
      }

      await axios.request(config)
      setUsers(users.filter((user) => user.id !== id))
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
        <title>{getPageTitle('Users')}</title>
      </Head>
      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiAccountMultiple}
          title="Users"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiTable} title="Overview"></SectionTitleLineWithButton>
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
            <TableUsers
              isSubmitting={isSubmitting}
              currentUser={currentUser}
              currentPage={currentPage}
              users={users}
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

UsersPage.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default UsersPage
