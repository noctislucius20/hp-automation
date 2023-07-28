import React from 'react'
import type { ReactElement } from 'react'
import Head from 'next/head'
import CardBox from '../components/CardBox'
import SectionFullScreen from '../components/SectionFullScreen'
import LayoutGuest from '../layouts/Guest'
import { Form, Formik } from 'formik'
import { flaskApiUrl, getPageTitle } from '../config'
import axios from 'axios'
import UsernameForm from '../components/RegisterForm/UsernameForm'
import PasswordForm from '../components/RegisterForm/PasswordForm'
import * as Yup from 'yup'
import NotificationBar from '../components/NotificationBar'
import { mdiAlertCircle, mdiClose } from '@mdi/js'
import { useRouter } from 'next/router'
import BaseButton from '../components/BaseButton'
import Image from 'next/image'
import logo from '../../public/logo.png'

const RegisterPage = () => {
  const [step, setStep] = React.useState(1)

  const router = useRouter()

  const initialValues = {
    username: '',
    firstName: '',
    lastName: '',
    password: '',
    confirmPassword: '',
  }

  const validationSchema = Yup.object().shape({
    username: Yup.string().required('Username is required'),
    firstName: Yup.string().required('First Name is required'),
    lastName: Yup.string().required('Last Name is required'),
    password: Yup.string()
      .required('Password is required')
      .min(6, 'Password must be at least 6 characters'),
    confirmPassword: Yup.string()
      .required('Confirm Password is required')
      .oneOf([Yup.ref('password'), null], 'Passwords must match'),
  })

  const handleRegister = async (values, { resetForm, setStatus }) => {
    try {
      delete values.confirmPassword

      await axios.post(`${flaskApiUrl}/users`, values)
      resetForm()

      router.push('/login')
    } catch (error) {
      console.log(error)
      resetForm()
      setStatus({ error: { message: error.response.data.message, code: error.response.status } })

      router.push('/register')
    }
  }

  const handleNext = () => {
    setStep(2)
    console.log(step)
  }

  const handleBack = () => {
    setStep(1)
    console.log(step)
  }

  return (
    <>
      <Head>
        <title>{getPageTitle('Register')}</title>
      </Head>

      <SectionFullScreen bg="purplePink">
        <CardBox className="w-11/12 md:w-7/12 lg:w-6/12 xl:w-4/12 shadow-2xl">
          <div className="grid justify-items-center">
            <Image src={logo} width={225} alt="" />
          </div>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleRegister}
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
                  {step === 1 && <UsernameForm onNext={handleNext} />}
                  {step === 2 && <PasswordForm onBack={handleBack} isSubmitting={isSubmitting} />}
                </Form>
              </>
            )}
          </Formik>
        </CardBox>
      </SectionFullScreen>
    </>
  )
}

RegisterPage.getLayout = function getLayout(page: ReactElement) {
  return <LayoutGuest>{page}</LayoutGuest>
}

export default RegisterPage
