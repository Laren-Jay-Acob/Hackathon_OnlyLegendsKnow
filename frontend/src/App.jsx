import React, {useState} from "react";
import Button from "./components/button/button.jsx";
import Enemy from "./components/enemy/Enemy.jsx";

const App = () => {
  
  const [coins, setCoins]  = useState(0);
  return (
    <div>
      <Enemy />
    </div>
  );
};

export default App;
