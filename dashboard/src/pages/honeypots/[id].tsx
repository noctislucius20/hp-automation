import { mdiAlertCircle, mdiArrowLeftThick, mdiBeehiveOutline, mdiClose, mdiPencil } from '@mdi/js'
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

const HoneypotDetails = () => {
  const router = useRouter()
  const { id } = router.query

  const [honeypot, setHoneypot] = useState({ name: '', description: '' })
  const [status, setStatus] = useState({ error: null, success: null })
  const [isLoading, setIsLoading] = useState(true)
  const [isReadOnly, setIsReadOnly] = useState(true)

  useEffect(() => {
    if (id) {
      const getHoneypot = async () => {
        try {
          const token = JSON.parse(localStorage.getItem('token'))
          const config = {
            headers: { Authorization: `Bearer ${token.access_token}` },
            method: 'GET',
            url: `${flaskApiUrl}/honeypots/${id}`,
          }

          const response = await axios.request(config)
          setHoneypot({
            name: response.data.data.name,
            description: response.data.data.description,
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
      getHoneypot()
    }
  }, [id])

  const initialValues = {
    name: honeypot ? honeypot.name : '',
    description: honeypot ? honeypot.description : '',
  }

  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Name is required'),
  })

  const handleHoneypotSubmit = async (values, { resetForm, setStatus }) => {
    try {
      const token = JSON.parse(localStorage.getItem('token'))
      const config = {
        headers: { Authorization: `Bearer ${token.access_token}` },
        method: 'PUT',
        url: `${flaskApiUrl}/honeypots/${id}`,
        data: values,
      }

      const response = await axios.request(config)
      setHoneypot(values)
      setIsReadOnly(true)

      setStatus({
        error: null,
        success: {
          message: response == undefined ? 'Data updated' : response.data.message,
          code: response == undefined ? 200 : response.status,
        },
      })

      router.push(`/honeypots/${id}`)
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

      router.push(`/honeypots/${id}`)
    }
  }

  return (
    <>
      <Head>
        <title>{getPageTitle(`Details: ${honeypot.name}`)}</title>
      </Head>

      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiBeehiveOutline}
          title="Honeypots"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiPencil} title={`Honeypot: ${honeypot.name}`}>
          <BaseButton
            href="/honeypots/overview"
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
              onSubmit={handleHoneypotSubmit}
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
                      <FormField label="Name" isTransparent={isReadOnly}>
                        <Field name="name" disabled={isReadOnly} />
                      </FormField>
                      <ErrorMessage
                        name="name"
                        component="div"
                        className="text-red-500 text-xs italic mb-4"
                      />

                      <FormField label="Description" isTransparent={isReadOnly}>
                        <Field name="description" disabled={isReadOnly} />
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

HoneypotDetails.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default HoneypotDetails
