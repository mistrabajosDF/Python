import axios from "axios";

const apiService = axios.create({
    baseURL: 'http://localhost:5000/',
    //baseURL: 'https://admin-grupo22.proyecto2023.linti.unlp.edu.ar/',
    withCredentials: true,
    xsrfCookieName: 'csrf_access_token',
    xsrfHeaderName: "X-CSRF-TOKEN",
});

export { apiService }