import { mdiAccount, mdiAlertCircle, mdiClose } from '@mdi/js'
import { Formik, Form, Field } from 'formik'
import Head from 'next/head'
import { ReactElement, useState } from 'react'
import BaseButton from '../components/BaseButton'
import BaseButtons from '../components/BaseButtons'
import CardBox from '../components/CardBox'
import CardBoxComponentBody from '../components/CardBoxComponentBody'
import CardBoxComponentFooter from '../components/CardBoxComponentFooter'
import FormField from '../components/FormField'
import LayoutAuthenticated from '../layouts/Authenticated'
import SectionMain from '../components/SectionMain'
import SectionTitleLineWithButton from '../components/SectionTitleLineWithButton'
import UserCard from '../components/UserCard'
import type { UserForm } from '../interfaces'
import { flaskApiUrl, getPageTitle } from '../config'
import { useAppSelector } from '../stores/hooks'
import NotificationBar from '../components/NotificationBar'
import axios from 'axios'
import jwt from 'jsonwebtoken'
import { useRouter } from 'next/router'

const ProfilePage = () => {
  const router = useRouter()

  const userName = useAppSelector((state) => state.main.userName)
  const userFirstName = useAppSelector((state) => state.main.userFirstName)
  const userLastName = useAppSelector((state) => state.main.userLastName)
  const userRoles = useAppSelector((state) => state.main.userRoles)

  const [isReadOnly, setIsReadOnly] = useState(true)
  const [status, setStatus] = useState({ error: null, success: null })

  const userForm: UserForm = {
    username: userName,
    firstName: userFirstName,
    lastName: userLastName,
    roles: userRoles,
  }

  const refreshJwtToken = async (username) => {
    try {
      const token = JSON.parse(localStorage.getItem('token'))
      const config = {
        method: 'PUT',
        url: `${flaskApiUrl}/auth`,
        data: {
          refresh_token: token.refresh_token,
          username: username,
          roles: userForm.roles,
        },
      }
      console.log(config)
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
        success: null,
      })
    }
  }

  const handleUserSubmit = async (values, { resetForm, setStatus }) => {
    try {
      const token = JSON.parse(localStorage.getItem('token'))
      const user = jwt.decode(token.access_token)
      const config = {
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
        method: 'PUT',
        url: `${flaskApiUrl}/users/${user.username}`,
        data: values,
      }
      console.log(user.username)
      const response = await axios.request(config)
      await refreshJwtToken(values.username)
      setIsReadOnly(true)

      // const config_token = {
      //   method: 'DELETE',
      //   url: `${flaskApiUrl}/auth`,
      //   data: { refresh_token: token.refresh_token },
      // }
      // await axios.request(config_token)
      // localStorage.removeItem('token')
      // localStorage.removeItem('expirationTime')

      setStatus({
        error: null,
        success: {
          message: response == undefined ? 'Data updated' : response.data.message,
          code: response == undefined ? 200 : response.status,
        },
      })

      router.push(`/profile`)
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

      router.push(`/profile`)
    }
  }
  return (
    <>
      <Head>
        <title>{getPageTitle('Profile')}</title>
      </Head>

      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiAccount}
          title="Profile"
          main
        ></SectionTitleLineWithButton>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <UserCard />
          <div className="flex flex-col">
            <CardBox className="flex-1" hasComponentLayout>
              <Formik initialValues={userForm} onSubmit={handleUserSubmit}>
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
                    <Form className="flex flex-col flex-1">
                      <CardBoxComponentBody>
                        <FormField label="Username" icons={[mdiAccount]} isTransparent={isReadOnly}>
                          <Field name="username" disabled={isReadOnly} />
                        </FormField>
                        <FormField
                          label="First Name"
                          icons={[mdiAccount]}
                          isTransparent={isReadOnly}
                        >
                          <Field name="firstName" disabled={isReadOnly} />
                        </FormField>
                        <FormField
                          label="Last Name"
                          icons={[mdiAccount]}
                          isTransparent={isReadOnly}
                        >
                          <Field name="lastName" disabled={isReadOnly} />
                        </FormField>
                      </CardBoxComponentBody>
                      <CardBoxComponentFooter>
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

                        {/* <BaseButtons>
                      <BaseButton color="info" type="submit" label="Submit" />
                      <BaseButton color="info" label="Options" outline />
                    </BaseButtons> */}
                      </CardBoxComponentFooter>
                    </Form>
                  </>
                )}
              </Formik>
            </CardBox>
          </div>
        </div>
      </SectionMain>
    </>
  )
}

ProfilePage.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default ProfilePage
