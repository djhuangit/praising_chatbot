import React from 'react';
import styled from '@emotion/styled';
import Chat from './components/Chat';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
`;

const Header = styled.header`
  background-color: #4a90e2;
  color: white;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const App: React.FC = () => {
  return (
    <AppContainer>
      <Header>
        <h1>KuaKua Qun</h1>
        <p>Your Supportive Chat Space</p>
      </Header>
      <Chat />
    </AppContainer>
  );
};

export default App; 