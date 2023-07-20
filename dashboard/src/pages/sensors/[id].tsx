import {
  mdiAlertCircle,
  mdiArrowLeftThick,
  mdiClose,
  mdiMonitorDashboard,
  mdiPencil,
  mdiRaspberryPi,
  mdiTextBoxOutline,
} from '@mdi/js'
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
import FormCheckRadioGroup from '../../components/FormCheckRadioGroup'
import FormCheckRadio from '../../components/FormCheckRadio'
import TableJobHistory from '../../components/TableJobHistory/TableJobHistory'

const SensorDetails = () => {
  const router = useRouter()
  const { id } = router.query

  const [sensor, setSensor] = useState({
    ipAddress: '',
    name: '',
    description: '',
    honeypot: [],
    dashboard_url: '',
  })
  const [honeypots, setHoneypots] = useState([])
  const [jobHistory, setJobHistory] = useState([])
  const [status, setStatus] = useState({ error: null })
  const [isLoading, setIsLoading] = useState(true)
  const [isReadOnly, setIsReadOnly] = useState(true)
  const [notifVisible, setNotifVisible] = useState(true)
  const [isJobRunning, setIsJobRunning] = useState(true)
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

  const handleResetStatus = () => {
    setStatus({ error: null })
  }

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  useEffect(() => {
    const getHoneypots = async () => {
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

  useEffect(() => {
    if (id) {
      const getSensor = async () => {
        try {
          if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
            await refreshJwtToken()
          }

          const token = JSON.parse(localStorage.getItem('token'))
          const configSensor = {
            headers: { Authorization: `Bearer ${token.access_token}` },
            method: 'GET',
            url: `${flaskApiUrl}/sensors/${id}`,
          }

          const response = await axios.request(configSensor)

          setSensor({
            ipAddress: response.data.data.ip_address,
            name: response.data.data.name,
            description: response.data.data.description,
            honeypot: response.data.data.honeypot,
            dashboard_url: response.data.data.dashboard_url,
          })

          if (
            response.data.data.job_history[0]['deployment_status'] === 'failed' ||
            response.data.data.job_history[0]['deployment_status'] === 'canceled' ||
            response.data.data.job_history[0]['deployment_status'] === 'successful' ||
            response.data.data.job_history[0]['deployment_status'] === 'error'
          ) {
            setIsJobRunning(false)
          }

          setJobHistory(response.data.data.job_history)
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
          setIsLoading(false)
        }
      }
      getSensor()
    }
  }, [id])

  const initialValues = {
    ipAddress: sensor.ipAddress ? sensor.ipAddress : '',
    name: sensor.name ? sensor.name : '',
    description: sensor.description ? sensor.description : '',
    honeypot: sensor.honeypot
      ? sensor.honeypot.map((obj) => `{'id': ${obj.id}, 'name': '${obj.name}'}`)
      : '',
  }

  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Name is required'),
    ipAddress: Yup.string().required('IP Address is required'),
    honeypot: Yup.array().required('Honeypots is required'),
  })

  const handleSensorSubmit = async (values, { resetForm, setStatus }) => {
    try {
      if (localStorage.getItem('expirationTime') < JSON.stringify(Date.now() / 1000)) {
        await refreshJwtToken()
      }

      const token = JSON.parse(localStorage.getItem('token'))
      const config = {
        headers: { Authorization: `Bearer ${token.access_token}` },
        method: 'PUT',
        url: `${flaskApiUrl}/sensors/${id}`,
        data: values,
      }

      await axios.request(config)
      setSensor(values)
      setIsReadOnly(true)

      router.push(`/sensors/overview`)
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

      router.push(`/sensors/${id}`)
    }
  }

  useEffect(() => {
    setTimeout(() => {
      setNotifVisible(false)
    }, 60000)
  }, [notifVisible])

  return (
    <>
      <Head>
        <title>{getPageTitle(`Details: ${sensor.name}`)}</title>
      </Head>

      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiRaspberryPi}
          title="Sensors"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiPencil} title={`Details: ${sensor.name}`}>
          <BaseButtons>
            <BaseButton
              href="/sensors/overview"
              icon={mdiArrowLeftThick}
              label="Back"
              color="danger"
              small
              roundedFull
            />
            <BaseButton
              href="/sensors/[id]/logs"
              as={`/sensors/${id}/logs`}
              icon={mdiTextBoxOutline}
              color="info"
              label="Logs"
              small
              roundedFull
            />
            <BaseButton
              href={sensor.dashboard_url}
              icon={mdiMonitorDashboard}
              color="warning"
              label="Monitor"
              disabled={isJobRunning}
              small
              roundedFull
              target="_blank"
            />
          </BaseButtons>
        </SectionTitleLineWithButton>
        {!isLoading && isJobRunning && !status.error && (
          <NotificationBar
            color="warning"
            icon={mdiAlertCircle}
            button={
              <BaseButton
                color="white"
                roundedFull
                small
                icon={mdiClose}
                // onClick={() => {
                //   setJobStatus(true)
                // }}
              />
            }
          >
            Deployment still in progress. Check logs for more details.
          </NotificationBar>
        )}
        {status && status.error && notifVisible && (
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
        <CardBox>
          {isLoading ? (
            <div>Loading...</div>
          ) : (
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
                    <>
                      <FormField label="Name" isTransparent={isReadOnly}>
                        <Field name="name" disabled={isReadOnly} />
                      </FormField>
                      <ErrorMessage
                        name="name"
                        component="div"
                        className="text-red-500 text-xs italic mb-4"
                      />

                      <FormField label="IP Address" isTransparent={isReadOnly}>
                        <Field name="ipAddress" disabled={isReadOnly} />
                      </FormField>
                      <ErrorMessage
                        name="ipAddress"
                        component="div"
                        className="text-red-500 text-xs italic mb-4"
                      />

                      <FormField label="Description" isTransparent={isReadOnly}>
                        <Field name="description" disabled={isReadOnly} />
                      </FormField>

                      <BaseDivider />

                      <FormField label="Honeypots" isTransparent={isReadOnly}>
                        <FormCheckRadioGroup>
                          {honeypots.map((hp, index) => (
                            <FormCheckRadio type="checkbox" label={hp.name} key={index}>
                              <>
                                <Field
                                  type="checkbox"
                                  name="honeypot"
                                  value={`{'id': ${hp.id}, 'name': '${hp.name}'}`}
                                  disabled={isReadOnly}
                                />
                              </>
                            </FormCheckRadio>
                          ))}
                        </FormCheckRadioGroup>
                      </FormField>

                      <BaseDivider />

                      <label className="block font-bold mb-2">Deployment History</label>
                      <CardBox className="mb-6" hasTable>
                        <TableJobHistory
                          jobHistory={jobHistory}
                          status={status}
                          currentPage={currentPage}
                          pageChange={handlePageChange}
                        />
                        {/* <p className={`${statusColor} text-base`}>
                          {jobStatus.charAt(0).toUpperCase() + jobStatus.slice(1)}
                        </p> */}
                      </CardBox>

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
                            disabled={isSubmitting || isJobRunning}
                          />
                        ) : (
                          <BaseButton
                            type="button"
                            color="danger"
                            label="Cancel"
                            onClick={() => setIsReadOnly(true)}
                            disabled={isSubmitting || isJobRunning}
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

SensorDetails.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default SensorDetails
