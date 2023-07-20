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
      <FormField label="Password" help="Please enter your password">
        <Field name="password" type="password" />
      </FormField>
      <ErrorMessage
        name="password"
        component="div"
        className="text-red-500 text-xs italic mt-2 mb-4"
      />

      <FormField label="Confirm Password" help="Confirm your password">
        <Field name="confirmPassword" type="password" />
      </FormField>
      <ErrorMessage
        name="confirmPassword"
        component="div"
        className="text-red-500 text-xs italic mt-2"
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
