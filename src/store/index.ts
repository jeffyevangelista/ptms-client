import {create} from 'zustand'
import {devtools} from 'zustand/middleware'
import createAuthSlice, { type AuthSlice } from './auth.slice'

type Store = AuthSlice
const useStore = create<Store>()(
    devtools((...a) => ({
        ...createAuthSlice(...a)
    }))
)

export default useStore