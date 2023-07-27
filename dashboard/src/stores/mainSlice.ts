import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { UserPayloadObject } from '../interfaces'

interface MainState {
  userName: string
  userFirstName: string
  userLastName: string
  userRoles: string
  userEmail: null | string
  userAvatar: null | string
  isFieldFocusRegistered: boolean
}

const initialState: MainState = {
  /* User */
  userName: '',
  userFirstName: '',
  userLastName: '',
  userRoles: '',
  userEmail: null,
  userAvatar: null,

  /* Field focus with ctrl+k (to register only once) */
  isFieldFocusRegistered: false,
}

export const mainSlice = createSlice({
  name: 'main',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<UserPayloadObject>) => {
      state.userName = action.payload.username
      state.userFirstName = action.payload.firstName
      state.userLastName = action.payload.lastName
      state.userRoles = action.payload.roles
      state.userEmail = action.payload.email
      state.userAvatar = action.payload.avatar
    },
  },
})

// Action creators are generated for each case reducer function
export const { setUser } = mainSlice.actions

export default mainSlice.reducer
