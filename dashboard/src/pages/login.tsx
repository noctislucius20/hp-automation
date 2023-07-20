import React from 'react'
import type { ReactElement } from 'react'
import Head from 'next/head'
import BaseButton from '../components/BaseButton'
import CardBox from '../components/CardBox'
import SectionFullScreen from '../components/SectionFullScreen'
import LayoutGuest from '../layouts/Guest'
import { ErrorMessage, Field, Form, Formik } from 'formik'
import FormField from '../components/FormField'
import BaseDivider from '../components/BaseDivider'
import BaseButtons from '../components/BaseButtons'
import { flaskApiUrl, getPageTitle } from '../config'
import axios from 'axios'
import { useRouter } from 'next/router'
import NotificationBar from '../components/NotificationBar'
import { mdiAlertCircle, mdiClose } from '@mdi/js'
import * as Yup from 'yup'
import jwt from 'jsonwebtoken'

const LoginPage = () => {
  const router = useRouter()

  const initialValues = {
    username: '',
    password: '',
  }

  const validationSchema = Yup.object().shape({
    username: Yup.string().required('Username is required'),
    password: Yup.string().required('Password is required'),
  })

  const handleLogin = async (values, { resetForm, setStatus }) => {
    try {
      const response = await axios.post(`${flaskApiUrl}/auth`, values)
      const accessToken = jwt.decode(response.data.data.access_token)
      localStorage.setItem('expirationTime', JSON.stringify(accessToken.exp))
      localStorage.setItem('token', JSON.stringify(response.data.data))
      console.log(response.data.data)
      resetForm()

      router.push('/dashboard')
    } catch (error) {
      console.log(error)
      resetForm()
      setStatus({
        error: {
          message:
            error.response == undefined ? 'Something went wrong' : error.response.data.message,
          code: error.response == undefined ? 500 : error.response.status,
        },
      })
      router.push('/login')
    }
  }

  return (
    <>
      <Head>
        <title>{getPageTitle('Login')}</title>
      </Head>

      <SectionFullScreen bg="purplePink">
        <CardBox className="w-11/12 md:w-7/12 lg:w-6/12 xl:w-4/12 shadow-2xl">
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleLogin}
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
                <Form>
                  <FormField label="Username" help="Please enter your username">
                    <Field name="username" />
                  </FormField>
                  <ErrorMessage
                    name="username"
                    component="div"
                    className="text-red-500 text-xs italic mb-4"
                  />

                  <FormField label="Password" help="Please enter your password">
                    <Field name="password" type="password" />
                  </FormField>
                  <ErrorMessage
                    name="password"
                    component="div"
                    className="text-red-500 text-xs italic mb-4"
                  />

                  <BaseDivider />

                  <BaseButtons className="justify-between">
                    <BaseButton type="submit" label="Login" color="info" disabled={isSubmitting} />
                    <BaseButton
                      type="button"
                      label="I don't have an account"
                      color="info"
                      outline
                      href="/register"
                      disabled={isSubmitting}
                    />
                  </BaseButtons>
                </Form>
              </>
            )}
          </Formik>
        </CardBox>
      </SectionFullScreen>
    </>
  )
}

LoginPage.getLayout = function getLayout(page: ReactElement) {
  return <LayoutGuest>{page}</LayoutGuest>
}

export default LoginPage
