import React, {useState} from "react";
import Button from "./components/button/button.jsx";

const App = () => {
  
  const [coins, setCoins]  = useState(0);
  return (
    <div className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] flex-col justify-center align-center items-center">
      <p className="text-center">{coins}</p>
      <Button></Button>
    </div>
  );
};

export default App;
