import React from 'react'
import FormField from '../FormField'
import { Field, ErrorMessage } from 'formik'
import BaseButton from '../BaseButton'
import BaseButtons from '../BaseButtons'
import BaseDivider from '../BaseDivider'

type Props = {
  onBack: () => void
  isSubmitting: boolean
}

const PasswordForm = (props: Props) => {
  return (
    <>
      <FormField label="Password">
        <Field name="password" type="password" />
      </FormField>
      <ErrorMessage name="password" component="div" className="text-red-500 text-xs italic mt-0" />

      <FormField label="Confirm Password">
        <Field name="confirmPassword" type="password" />
      </FormField>
      <ErrorMessage
        name="confirmPassword"
        component="div"
        className="text-red-500 text-xs italic mt-0"
      />

      <BaseDivider />

      <BaseButtons className="justify-between">
        <BaseButton type="submit" label="Register" color="info" disabled={props.isSubmitting} />
        <BaseButton
          type="submit"
          label="Back"
          color="info"
          outline
          onClick={() => {
            props.onBack()
          }}
        />
      </BaseButtons>
    </>
  )
}

export default PasswordForm
