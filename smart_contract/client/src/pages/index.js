import { Button, Heading, VStack, Box, Flex, Spacer, Menu, MenuButton, MenuList, MenuItem, SimpleGrid } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import Web3 from 'web3';
import { abi as contractABI } from '../../../build/contracts/CertificateManagement.json';
import { Card, CardHeader, CardBody, CardFooter } from '@chakra-ui/react';

const NavBar = () => {
  return (
    <Flex p={4} bg="black" direction="column">
      <Box>
        {/* */}
      </Box>
      <Spacer />
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
    <Flex>
      <NavBar />
      <VStack
        spacing={4}
        align="center"
        justify="center"
        h="100vh"
        backgroundImage="/background.jpg"
        backgroundSize="cover"
      >
        <div style={{ backgroundColor: 'rgba(2, 2, 0, 0.8)', padding: '20px', borderRadius: '8px', width: '100%' }}>
          <Heading mb={8}>Certificate Management System</Heading>
          <Flex w="100%" justify="space-between">
            <VStack spacing={4} align="flex-start" w="48%">
              <Heading mb={4}>Your Certificates</Heading>
              <SimpleGrid columns={1} gap={8} w="100%" justifyItems="center">
                <CardSection title="Certificate 1" onClick={() => getCerti(1)} />
                <CardSection title="Certificate 2" onClick={() => getCerti(2)} />
                <CardSection title="Certificate 3" onClick={() => getCerti(3)} />
              </SimpleGrid>
            </VStack>
            <VStack spacing={4} align="flex-start" w="48%">
              <Heading mb={4}>Nominee Certificates</Heading>
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
          <Button colorScheme="purple" onClick={getCount}>
            See Count
          </Button>
          <Button colorScheme="green" onClick={setCount}>
            Increase Count
          </Button>
        </div>
      </VStack>
    </Flex>
  );
}
