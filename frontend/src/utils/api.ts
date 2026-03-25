import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getRecommendations = async (userId: string) => {
  const response = await apiClient.get(`/recommendations/${userId}`)
  return response.data
}

export const getBiasProfile = async (userId: string) => {
  const response = await apiClient.get(`/bias-profile/${userId}`)
  return response.data
}

export const analyzeAsset = async (assetId: string) => {
  const response = await apiClient.post('/analyze', { assetId })
  return response.data
}

export default apiClient
