import { mdiAlertCircle, mdiArrowLeftThick, mdiBeehiveOutline, mdiClose, mdiPlusBox } from '@mdi/js'
import { ErrorMessage, Field, Form, Formik } from 'formik'
import Head from 'next/head'
import { ReactElement, useState } from 'react'
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

const HoneypotsCreate = () => {
  const router = useRouter()

  const [status, setStatus] = useState({ error: null })

  const initialValues = {
    name: '',
    description: '',
  }

  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Name is required'),
  })

  const handleHoneypotSubmit = async (values, { resetForm, setStatus }) => {
    try {
      const token = JSON.parse(localStorage.getItem('token'))

      const config = {
        method: 'POST',
        url: `${flaskApiUrl}/honeypots`,
        data: values,
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
      }

      await axios.request(config)
      resetForm()

      router.push('/honeypots/overview')
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

      router.push('/honeypots/add')
    }
  }

  return (
    <>
      <Head>
        <title>{getPageTitle('Forms')}</title>
      </Head>

      <SectionMain>
        <SectionTitleLineWithButton
          icon={mdiBeehiveOutline}
          title="Honeypots"
          main
        ></SectionTitleLineWithButton>

        <SectionTitleLineWithButton icon={mdiPlusBox} title="Add New Honeypot">
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
                <Form>
                  <FormField label="Name" help="Please enter honeypot name">
                    <Field name="name" />
                  </FormField>
                  <ErrorMessage
                    name="name"
                    component="div"
                    className="text-red-500 text-xs italic mb-4"
                  />

                  <FormField label="Description" help="Please enter honeypot description">
                    <Field name="description" />
                  </FormField>

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

HoneypotsCreate.getLayout = function getLayout(page: ReactElement) {
  return <LayoutAuthenticated>{page}</LayoutAuthenticated>
}

export default HoneypotsCreate
