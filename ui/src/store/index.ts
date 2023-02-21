import { createStore } from 'vuex'

export const store = createStore({
  state: {
    userData:  {
        userId: "",
        accountId: "",
        email: "",
        subdomain:""
    },
    pageStatusValue:  {
        urlValue: '',
        isS2SCompleted: false,
        isConfigCompleted: false
    }
  },
  getters: {
    getUser: (state, {dispatch}) =>  {
        return state.userData ;
      },
    
      getPageStatus:(state, {dispatch})=>{
        return state.pageStatusValue ;
      }
  },
  mutations: {
    setUserData: (state, payload) => { state.userData = payload },
    setPageStatus: (state, payload) => { state.pageStatusValue = payload }

  },
  actions: {}
});

export interface IUserInfo {
    userId: string,
    accountId: string,
    email: string,
    subdomain:string,
};

export interface IPageStatus {
    urlValue: string,
    isS2SCompleted: boolean,
    isConfigCompleted: boolean
}