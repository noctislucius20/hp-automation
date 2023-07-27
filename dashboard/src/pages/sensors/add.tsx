import { mdiAlertCircle, mdiArrowLeftThick, mdiClose, mdiPlusBox, mdiRaspberryPi } from '@mdi/js'
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
import FormCheckRadio from '../../components/FormCheckRadio'
import FormCheckRadioGroup from '../../components/FormCheckRadioGroup'

const SensorsCreate = () => {
  const router = useRouter()

  const [status, setStatus] = useState({ error: null })
  const [honeypots, setHoneypots] = useState([])

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
        console.log(response.data.data)
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

  const initialValues = {
    ipAddress: '',
    name: '',
    description: '',
    honeypot: '',
  }

  const validationSchema = Yup.object().shape({
    ipAddress: Yup.string().required('IP Address is required'),
    name: Yup.string().required('Name is required'),
    honeypot: Yup.array().required('Honeypots is required'),
  })

  // const handleSensorSubmit = async (values) => {
  //   console.log(values)
  // }

  const handleSensorSubmit = async (values, { resetForm, setStatus }) => {
    try {
      const token = JSON.parse(localStorage.getItem('token'))

      const config = {
        method: 'POST',
        url: `${flaskApiUrl}/sensors`,
        data: values,
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
      }

      await axios.request(config)
      resetForm()

      router.push('/sensors/overview')
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

      router.push('/sensors/add')
    }
  }

  return (
    <>
      <Head>
        <title>{getPageTitle('Forms')}</title>
      </Head>

      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiRaspberryPi}
          title="Sensors"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiPlusBox} title="Add New Sensor">
          <BaseButton
            href="/sensors/overview"
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
                  setStatus({ error: null })
                }}
              />
            }
          >
            Error {status.error.code}: {status.error.message}
          </NotificationBar>
        )}
        <CardBox>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSensorSubmit}
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
                  <FormField label="Name" help="Please enter sensor name">
                    <Field name="name" />
                  </FormField>
                  <ErrorMessage
                    name="name"
                    component="div"
                    className="text-red-500 text-xs italic mb-4"
                  />

                  <FormField label="IP Address" help="Please enter sensor IP Address">
                    <Field name="ipAddress" />
                  </FormField>
                  <ErrorMessage
                    name="name"
                    component="div"
                    className="text-red-500 text-xs italic mb-4"
                  />

                  <FormField label="Description" help="Please enter sensor description">
                    <Field name="description" />
                  </FormField>

                  <BaseDivider />

                  <FormField label="Honeypots">
                    <FormCheckRadioGroup>
                      {honeypots.map((hp, index) => (
                        <FormCheckRadio type="checkbox" label={hp.name} key={index}>
                          <>
                            <Field
                              type="checkbox"
                              name="honeypot"
                              value={`{'id': ${hp.id}, 'name': '${hp.name}'}`}
                            />
                          </>
                        </FormCheckRadio>
                      ))}
                    </FormCheckRadioGroup>
                  </FormField>
                  <ErrorMessage
                    name="honeypot"
                    component="div"
                    className="text-red-500 text-xs italic mb-4"
                  />
                  <BaseDivider />

                  <BaseButtons>
                    <BaseButton type="submit" color="info" label="Submit" disabled={isSubmitting} />
                  </BaseButtons>
                </Form>
              </>
            )}
          </Formik>
        </CardBox>
      </SectionMain>
    </>
  )
}

SensorsCreate.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default SensorsCreate
