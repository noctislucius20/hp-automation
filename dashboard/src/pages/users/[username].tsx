import { mdiAccountMultiple, mdiAlertCircle, mdiArrowLeftThick, mdiClose, mdiPencil } from '@mdi/js'
import { ErrorMessage, Field, Form, Formik } from 'formik'
import Head from 'next/head'
import { ReactElement, useEffect, useState } from 'react'
import BaseButton from '../../components/BaseButton'
import BaseButtons from '../../components/BaseButtons'
import BaseDivider from '../../components/BaseDivider'
import CardBox from '../../components/CardBox'
import FormField from '../../components/FormField'
import LayoutAuthenticated from '../../layouts/Authenticated'
import SectionMain from '../../components/SectionMain'
import SectionTitleLineWithButton from '../../components/SectionTitleLineWithButton'
import { flaskApiUrl, getPageTitle } from '../../config'
import * as Yup from 'yup'
import NotificationBar from '../../components/NotificationBar'
import axios from 'axios'
import { useRouter } from 'next/router'
import jwt from 'jsonwebtoken'

const UserDetails = () => {
  const router = useRouter()
  const { username } = router.query

  const [user, setUser] = useState({ username: '', firstName: '', lastName: '', roles: '' })
  const [status, setStatus] = useState({ error: null, success: null })
  const [isLoading, setIsLoading] = useState(true)
  const [isReadOnly, setIsReadOnly] = useState(true)
  const [currentUser, setCurrentUser] = useState('')

  // refresh token if expired
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
      if (accessToken.roles === 'admin') {
        setCurrentUser('admin')
      }

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
        success: null,
      })
    }
  }

  // get user details
  useEffect(() => {
    if (username) {
      const getUser = async () => {
        try {
          if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
            await refreshJwtToken()
          }

          const token = JSON.parse(localStorage.getItem('token'))
          const config = {
            headers: {
              Authorization: `Bearer ${token.access_token}`,
            },
            method: 'GET',
            url: `${flaskApiUrl}/users/${username}`,
          }

          const response = await axios.request(config)
          console.log(response)
          setUser({
            username: response.data.data.username,
            firstName: response.data.data.first_name,
            lastName: response.data.data.last_name,
            roles: response.data.data.roles,
          })
          setIsLoading(false)
        } catch (error) {
          console.log(error)
          setStatus({
            error: {
              message:
                error.response == undefined ? 'Something went wrong' : error.response.data.message,
              code: error.response == undefined ? 500 : error.response.status,
            },
            success: null,
          })
          setIsLoading(false)
        }
      }
      getUser()
    }
  }, [username])

  // set initial values
  const initialValues = {
    username: user ? user.username : '',
    firstName: user ? user.firstName : '',
    lastName: user ? user.lastName : '',
    roles: user ? user.roles : '',
  }

  // set validation schema
  const validationSchema = Yup.object().shape({
    roles: Yup.string().required('roles is required'),
  })

  // handle user submit
  const handleUserSubmit = async (values, { resetForm, setStatus }) => {
    try {
      if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
        await refreshJwtToken()
      }

      const token = JSON.parse(localStorage.getItem('token'))
      const config = {
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
        method: 'PUT',
        url: `${flaskApiUrl}/users/${username}`,
        data: values,
      }

      const response = await axios.request(config)
      setUser(values)
      setIsReadOnly(true)

      setStatus({
        error: null,
        success: {
          message: response == undefined ? 'Data updated' : response.data.message,
          code: response == undefined ? 200 : response.status,
        },
      })

      router.push(`/users/${username}`)
    } catch (error) {
      console.log(error)
      resetForm()
      setStatus({
        error: {
          message:
            error.response == undefined ? 'Something went wrong' : error.response.data.message,
          code: error.response == undefined ? 500 : error.response.status,
        },
        success: null,
      })

      router.push(`/users/${username}`)
    }
  }

  return (
    <>
      <Head>
        <title>{getPageTitle(`Details: ${user.username}`)}</title>
      </Head>

      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiAccountMultiple}
          title="Users"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiPencil} title={`User: ${user.username}`}>
          <BaseButton
            href="/users/overview"
            icon={mdiArrowLeftThick}
            label="Back"
            color="danger"
            small
            roundedFull
          />
        </SectionTitleLineWithButton>

        {status && status.error && (
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
                  setStatus({ error: null, success: null })
                }}
              />
            }
          >
            Error {status.error.code}: {status.error.message}
          </NotificationBar>
        )}
        <CardBox>
          {isLoading ? (
            <div>Loading...</div>
          ) : (
            <Formik
              initialValues={initialValues}
              validationSchema={validationSchema}
              onSubmit={handleUserSubmit}
            >
              {({ isSubmitting, status, setStatus }) => (
                <>
                  {status && status.error && (
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
                            setStatus('')
                          }}
                        />
                      }
                    >
                      Error {status.error.code}: {status.error.message}
                    </NotificationBar>
                  )}
                  {status && status.success && (
                    <NotificationBar
                      color="success"
                      icon={mdiAlertCircle}
                      button={
                        <BaseButton
                          color="white"
                          roundedFull
                          small
                          icon={mdiClose}
                          onClick={() => {
                            setStatus({ error: null, success: null })
                          }}
                        />
                      }
                    >
                      Success: {status.success.message}
                    </NotificationBar>
                  )}
                  <Form>
                    <>
                      <FormField
                        label="Username"
                        // isTransparent={currentUser === 'admin' ? true : false}
                        isTransparent={true}
                      >
                        {/* <Field name="username" disabled={currentUser === 'admin' ? true : false} /> */}
                        <Field name="username" disabled={true} />
                      </FormField>
                      <ErrorMessage
                        name="username"
                        component="div"
                        className="text-red-500 text-xs italic mb-4"
                      />
                      <FormField
                        label="First Name"
                        // isTransparent={currentUser === 'admin' ? true : false}
                        isTransparent={true}
                      >
                        {/* <Field name="firstName" disabled={currentUser === 'admin' ? true : false} /> */}
                        <Field name="firstName" disabled={true} />
                      </FormField>
                      <FormField
                        label="Last Name"
                        // isTransparent={currentUser === 'admin' ? true : false}
                        isTransparent={true}
                      >
                        {/* <Field name="lastName" disabled={currentUser === 'admin' ? true : false} /> */}
                        <Field name="lastName" disabled={true} />
                      </FormField>
                      <FormField label="Roles" isTransparent={isReadOnly}>
                        <Field name="roles" id="roles" component="select" disabled={isReadOnly}>
                          <option value="admin">admin</option>
                          <option value="user">user</option>
                        </Field>
                      </FormField>
                      <BaseDivider />
                      <BaseButtons>
                        <BaseButton
                          type="submit"
                          color="info"
                          label="Save"
                          disabled={isReadOnly || isSubmitting}
                        />
                        {isReadOnly ? (
                          <BaseButton
                            type="button"
                            color="warning"
                            label="Edit"
                            onClick={() => setIsReadOnly(false)}
                            disabled={isSubmitting}
                          />
                        ) : (
                          <BaseButton
                            type="button"
                            color="danger"
                            label="Cancel"
                            onClick={() => setIsReadOnly(true)}
                            disabled={isSubmitting}
                          />
                        )}
                      </BaseButtons>
                    </>
                  </Form>
                </>
              )}
            </Formik>
          )}
        </CardBox>
      </SectionMain>
    </>
  )
}

UserDetails.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default UserDetails
