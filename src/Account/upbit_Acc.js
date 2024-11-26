import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
 
dotenv.config();
 
const access_key = process.env.UPBIT_OPEN_API_ACCESS_KEY;
const secret_key = process.env.UPBIT_OPEN_API_SECRET_KEY;
const server_url = process.env.UPBIT_OPEN_API_SERVER_URL;
 
const getMyAccount = async () => {
  const payload = {
    access_key: access_key,
    nonce: uuidv4(),
  };
 
  const token = jwt.sign(payload, secret_key);
  const options = {
    method: "GET",
    url: `${server_url}/v1/accounts`,
    headers: { Authorization: `Bearer ${token}` },
  };
 
  try {
    const response = await axios(options);
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};
 
export default getMyAccount;