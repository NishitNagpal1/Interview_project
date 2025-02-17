import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

// Get questions from the backend
export const getQuestions = async (count = 1) => {
    const response = await axios.get(`${API_BASE_URL}/questions?count=${count}`);
    return response.data.questions;
};

// Submit the answer
export const submitAnswer = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/submit`, data);  // Use POST for submitting answers
    return response.data;
};
