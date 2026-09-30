// src/types/quotation.ts

export interface Client {
  id?: number
  name: string
  email: string
  phone?: string
  company?: string
  status?: string
  created_at?: string
}

export interface LineItem {
  service: string
  price: number      // make sure backend uses `price`, not `prince`
}

export interface InquiryDetails {
  id: number
  service?: string
  client_details?: Client
}

export interface Quotation {
  id: number
  quotation_number: string
  amount: string
  description?: string
  valid_until: string
  status: 'pending' | 'approved' | 'rejected'
  inquiry: number
  inquiry_details?: InquiryDetails
  line_items?: LineItem[]
  created_at: string
}
