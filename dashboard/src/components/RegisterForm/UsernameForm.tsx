import React from 'react'
import FormField from '../FormField'
import { Field, ErrorMessage } from 'formik'
import BaseButton from '../BaseButton'
import BaseButtons from '../BaseButtons'
import BaseDivider from '../BaseDivider'

type Props = {
  onNext: () => void
}

const UsernameForm = (props: Props) => {
  return (
    <>
      <FormField label="Username" help="Please enter your username">
        <Field name="username" />
      </FormField>
      <ErrorMessage name="username" component="div" className="text-red-500 text-xs italic mb-4" />

      <FormField label="First Name" help="Please enter your first name">
        <Field name="firstName" />
      </FormField>
      <ErrorMessage name="firstName" component="div" className="text-red-500 text-xs italic mb-4" />

      <FormField label="Last Name" help="Please enter your last name">
        <Field name="lastName" />
      </FormField>
      <ErrorMessage name="lastName" component="div" className="text-red-500 text-xs italic " />

      <BaseDivider />

      <BaseButtons className="justify-start">
        <BaseButton
          type="submit"
          label="Next"
          color="info"
          onClick={() => {
            props.onNext()
          }}
        />
      </BaseButtons>
    </>
  )
}

export default UsernameForm
