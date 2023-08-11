export const localStorageDarkModeKey = 'darkMode'

export const localStorageStyleKey = 'style'

export const containerMaxW = 'xl:max-w-6xl xl:mx-auto'

export const appTitle = 'HoneypotExpress'

export const getPageTitle = (currentPageTitle: string) => `${currentPageTitle} - ${appTitle}`

export const flaskApiUrl =
  process.env.NODE_ENV === 'production'
    ? 'http://192.168.195.195:8080/api/v1'
    : 'http://localhost:5000/api/v1'
