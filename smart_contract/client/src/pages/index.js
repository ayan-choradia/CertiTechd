import Image from 'next/image'
import { Inter } from 'next/font/google'
import Web3 from 'web3';
import HDWalletProvider from '@truffle/hdwallet-provider';
import { abi as contractABI, networks } from "../../../build/contracts/CertificateManagement.json"
import { useEffect, useState } from 'react';
// import auth from "./api/hello.js";
import axios from 'axios';
import { getCookie, setCookie } from 'cookies-next';


const inter = Inter({ subsets: ['latin'] })

export default function Home() {

  const [web3, setWeb3] = useState(null);
  const [account, setAccount] = useState('0x');
  const [contractInstance, setContractInstance] = useState(null);
  const contractAddress = '0x55f60e1f70af9f2c6f8e71335872ecf5610e5d65'; // Replace with your contract's address

  useEffect(() => {
    if (typeof window !== 'undefined' && typeof window.ethereum !== 'undefined') {
      const newWeb3 = new Web3(window.ethereum);
      setWeb3(newWeb3);
      // Requesting access to user accounts using eth_requestAccounts
      window.ethereum.request({ method: 'eth_requestAccounts' })
        .then(accounts => {
          setAccount(accounts[0]);
          const fetchData = async (account) => {
            try {
              const response = await axios.post('/api/proxy', {
                wallet_address: account, // Replace with your wallet address
              });
              console.log('Response:', response.data);
              setCookie('access_token',response.data.access_token,{});
            } catch (error) {
              console.error('Error:', error.message);
            }
          };
          if(!getCookie('access_token')){
            fetchData(accounts[0]);
          }
        })
        .catch(error => {
          console.error('Error requesting accounts:', error);
        });
    }
  }, []);

  const getABI = () => {
    console.log(contractABI);
  }
  useEffect(() => {
    if (web3) {
      web3.eth.getAccounts().then(res => {
        setAccount(res[0]);
        setContractInstance(new web3.eth.Contract(contractABI, contractAddress));
      });
    }
  }, [web3]);


  const getCerti = async () => {
    console.log(account, contractInstance);
    try {
      const result = await contractInstance.methods.hasRole(Web3.utils.toChecksumAddress(account)).call();
      console.log(result);
    } catch (err) {
      console.log(err);
    }
  };

  const createCerti = async () => {
    console.log(account);
    try {
      const currentTimeInSeconds = Math.floor(Date.now() / 1000);
      const oneYearInSeconds = 365 * 24 * 60 * 60; // One year in seconds
      const receipt = await contractInstance.methods.createCertificate(
        Web3.utils.toChecksumAddress(account),
        "certificate for property",
        currentTimeInSeconds,
        currentTimeInSeconds + oneYearInSeconds
      ).send({ from: account });

      console.log('Transaction successful:', receipt);
      // Optionally perform actions after a successful transaction
      // window.location.reload();
    } catch (error) {
      console.error('Transaction error:', error);
    }
  }

  const getCount = async () => {
    const receipt = await contractInstance.methods.getTempCount().call();
    console.log(receipt);
  }

  const setCount = async () => {
    const receipt = await contractInstance.methods.setTempCount().send({ from: account });
    console.log(receipt);
  }

  const updateRole = async () => {
    const receipt = await contractInstance.methods.updateRole(Web3.utils.toChecksumAddress('0x1292d38AF161Bc60c70bB19057b633087caDEF4B'),"industry").send({ from: account });
    console.log(receipt);
  }

  const seeRole = async () => {
    const receipt = await contractInstance.methods.hasRole(Web3.utils.toChecksumAddress('0xcA122220458374aa8A6BCDbA3DA66DaFA3834FCe')).call();
    console.log(receipt);
  }


  return (
    <>
      <button onClick={getCerti}>click me!!</button>
      <br></br>
      <button onClick={createCerti}>generate a new Certificate</button>
      <br></br>
      <button onClick={getABI}>See ABI</button><br></br>
      <button onClick={getCount}>see Count</button><br></br>
      <button onClick={setCount}>increase count</button><br></br>
      <button onClick={updateRole}>updateRole</button><br></br>
      <button onClick={seeRole}>seeRole</button>

    </>

  )
}
