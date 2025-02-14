import axios from "axios"

const API_BASE_URL = "http://localhost:8000";

export const getQuestions = async( count=10) => {
    const response =await axios.get('${API_BASE_URL}/questions?count=${count}');
    return response.data;
};

export const submitAnswer =async (data) => {
    const response = await axios.get('${API_BASE_URL}/questions?count=${count}');
    return response.data;
};