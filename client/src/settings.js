import dotenv from "dotenv";

if (process.env.NODE_ENV === "production") {
    const result = dotenv.config();

    if (result.error)
        throw result.error;
}

const settings = {
    BASE_URL: process.env.BASE_URL || 'http://localhost:8000',
    API_VERSION: process.env.BASE_URL || 'v1'
};

export default settings;