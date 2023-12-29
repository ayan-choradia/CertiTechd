"use client"
import axios from 'axios';
import { getCookie, setCookie } from 'cookies-next';
import { Button, Heading, VStack, Box, Flex, Spacer, Menu, MenuButton, MenuList, MenuItem, SimpleGrid } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import Web3 from 'web3';
import { abi as contractABI } from '../../../build/contracts/CertificateManagement.json';
import { Card, CardHeader, CardBody, CardFooter } from '@chakra-ui/react';
import * as z from "zod"
import { useForm } from "react-hook-form"
import { Button1 } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { toast } from "@/components/ui/use-toast"


const NavBar = () => {
  return (
    <Flex p={4} bg="black" justify="space-between" align="center">
      <Box>
        <Heading color="black">Logo</Heading>
      </Box>
      <Box>
        <Menu>
          <MenuButton as={Button} color="white">
            Menu
          </MenuButton>
          <MenuList>
            <MenuItem>Option 1</MenuItem>
            <MenuItem>Option 2</MenuItem>
            <MenuItem>Option 3</MenuItem>
          </MenuList>
        </Menu>
      </Box>
    </Flex>
  );
};

const formSchema = z.object({
  username: z.string().min(2).max(50),
})

const CardSection = ({ title, onClick }) => {
  return (
    <Card w="640px">
      <CardHeader>{title}</CardHeader>
      <CardBody>
        {/* Card Body Content */}
      </CardBody>
      <CardFooter>
        <Button onClick={onClick}>Action</Button>
      </CardFooter>
    </Card>
  );
};

export function InputForm() {
  const form = useForm({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      username: "",
    },
  });
  // import auth from "./api/hello.js";


  function onSubmit(data) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }
}

export default function Home() {
  const [web3, setWeb3] = useState(null);
  const [account, setAccount] = useState('0x');
  const [contractInstance, setContractInstance] = useState(null);
  const contractAddress = '0x55f60e1f70af9f2c6f8e71335872ecf5610e5d65'; // Replace me with your contract address

  useEffect(() => {
    if (typeof window !== 'undefined' && typeof window.ethereum !== 'undefined') {
      const newWeb3 = new Web3(window.ethereum);
      setWeb3(newWeb3);
      // Requesting access to user accounts using eth_requestAccounts
      window.ethereum
        .request({ method: 'eth_requestAccounts' })
        .then((accounts) => {
          setAccount(accounts[0]);
          const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000',
          };
          const fetch = async () => {
            const response = await axios.post(
              'http://localhost:8000/api/v1/users/auth',
              { wallet_address: accounts[0] },
              {
                headers: headers,
              }
            );
            console.log(response);
          };
          fetch();
        })
        .catch((error) => {
          console.error('Error requesting accounts:', error);
        });
    }
  }, []);

  useEffect(() => {
    if (web3) {
      web3.eth.getAccounts().then((res) => {
        setAccount(res[0]);
        setContractInstance(new web3.eth.Contract(contractABI, contractAddress));
      });
    }
  }, [web3]);

  const getCerti = async () => {
    try {
      const result = await contractInstance.methods.hasRole(Web3.utils.toChecksumAddress(account)).call();
      console.log(result);
      // Replace this with actual logic to fetch certificate details
      console.log('Fetching certificate details...');
    } catch (err) {
      console.log(err);
    }
  };

  const createCerti = async () => {
    try {
      const currentTimeInSeconds = Math.floor(Date.now() / 1000);
      const oneYearInSeconds = 365 * 24 * 60 * 60; // One year in seconds
      const receipt = await contractInstance.methods
        .createCertificate(
          Web3.utils.toChecksumAddress(account),
          'certificate for property',
          currentTimeInSeconds,
          currentTimeInSeconds + oneYearInSeconds
        )
        .send({ from: account });

      console.log('Transaction successful:', receipt);
      // Optionally perform actions after a successful transaction
      // window.location.reload();
    } catch (error) {
      console.error('Transaction error:', error);
    }
  };


  const getCount = async () => {
    const receipt = await contractInstance.methods.getTempCount().call();
    console.log(receipt);
  };

  const setCount = async () => {
    const receipt = await contractInstance.methods.setTempCount().send({ from: account });
    console.log(receipt);
  };

  return (

    <Flex direction="column">
      <NavBar />
      <VStack
        spacing={4}
        align="center"
        justify="center"
        h="100vh"
        backgroundImage="/background.jpg"
        backgroundSize="cover"
      >
        <Box
          bgGradient="linear(to-b, #333333)"
          p={4}
          borderRadius="9px"
          width="100%"
        >
          {/* Designer Box for Heading */}
          <Box
            bg="black"
            color="white"
            borderRadius="9px"
            p={4}
            mb={8}
            textAlign="center"
          >
            <Heading>Certificate Management System</Heading>
          </Box>

          <Flex w="100%" justify="space-between">
            <VStack spacing={4} align="flex-start" w="48%">
              <Heading mb={4} color="black">Your Certificates</Heading>
              <SimpleGrid columns={1} gap={8} w="100%" justifyItems="center">
                <CardSection title="Certificate 1" onClick={() => getCerti(1)} />
                <CardSection title="Certificate 2" onClick={() => getCerti(2)} />
                <CardSection title="Certificate 3" onClick={() => getCerti(3)} />
              </SimpleGrid>
            </VStack>
            <VStack spacing={4} align="flex-start" w="48%">
              <Heading mb={4} color="black">Nominee Certificates</Heading>
              <SimpleGrid columns={1} gap={8} w="100%" justifyItems="center">
                <CardSection title="Nominee 1" onClick={() => getCerti(4)} />
                <CardSection title="Nominee 2" onClick={() => getCerti(5)} />
                <CardSection title="Nominee 3" onClick={() => getCerti(6)} />
              </SimpleGrid>
            </VStack>
          </Flex>
          <Button colorScheme="blue" onClick={createCerti}>
            Generate a new Certificate
          </Button>
          <Button colorScheme="purple" onClick={getCerti}>
            See Count
          </Button>
          <Button colorScheme="green" onClick={setCount}>
            Increase Count
          </Button>

        </Box>
      </VStack>
    </Flex>


  );
}
