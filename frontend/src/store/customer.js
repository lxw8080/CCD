import { defineStore } from 'pinia'

export const useCustomerStore = defineStore('customer', {
  state: () => ({
    currentCustomer: null,
    customerList: [],
    searchKeyword: '',
    statusFilter: ''
  }),
  
  actions: {
    setCurrentCustomer(customer) {
      this.currentCustomer = customer
    },
    
    setCustomerList(list) {
      this.customerList = list
    },
    
    setSearchKeyword(keyword) {
      this.searchKeyword = keyword
    },
    
    setStatusFilter(status) {
      this.statusFilter = status
    }
  }
})

