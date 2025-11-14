import React, { useEffect, useState } from "react";

const Game = () => {
  // Logic
  const [level, setLevel] = useState(1);
  const [hp, setHp] = useState(2);
  const [coins, setCoins] = useState(0);
  const [damage, setDamage] = useState(1);
  const [itemDamageLevel, setItemDamageLevel] = useState(0);
  const [itemDamagePrice, setItemDamagePrice] = useState(50);
  const [itemAutoClickLevel, setItemAutoClickLevel] = useState(1);
  const [autoClickInterval, setAutoClickInterval] = useState(3300);
  const [itemAutoClickPrice, setItemAutoClickPrice] = useState(50);

  const BaseHP = () => level * 2;

  useEffect(() => {
    if (hp <= 0) {
      setLevel((prev) => prev + 1);
      setHp(BaseHP);
      setCoins((prev) => prev + 10);
    }
  }, [hp]);

  // Auto Click Interval
  useEffect(() => {
    const itemAutoClickInterval = setInterval(() => {
      if (itemAutoClickLevel > 0) {
        handleClickDamage();
      }
    }, autoClickInterval);

    return () => clearInterval(itemAutoClickInterval);
  }, [itemAutoClickLevel]);

  // Click Logic
  const handleClickDamage = () => {
    setHp((prev) => prev - damage);
  };

  // Shop
  // item Add Damage
  const itemAddDamage = () => {
    if (coins >= itemDamagePrice) {
      setCoins((prev) => prev - itemDamagePrice);
      setDamage((d) => d + 1);
      setItemDamagePrice((prev) => Math.floor(prev * 1.5));
    }
  };

  // item Auto Clicker
  const buyAutoClicker = () => {
    if (coins >= itemAutoClickPrice) {
      console.log("Buy Auto Clicker...");
      setCoins((prev) => prev - itemAutoClickPrice);
      setItemAutoClickLevel((prev) => prev + 1);
      setItemAutoClickPrice((prev) => Math.floor(prev * 1.5));
      if (autoClickInterval > 0.75) {
        setAutoClickInterval(prev => prev - 300);
      }
    }
  };

  return (
    <main>
      {/* Nav */}

      {/* Level & Coins */}
      <section className="flex justify-between px-5 text-xl">
        <span className="">Level: {level}</span>
        <span className="text-amber-400 font-bold ">Coins: {coins}</span>
      </section>

      {/* Enemy */}
      <section className="flex justify-center mt-20">
        <button
          className="size-50 rounded-full bg-amber-500 transform transition-transform active:scale-80 duration-200"
          onClick={handleClickDamage}
        >
          Enemy
        </button>
      </section>

      {/* Stats */}
      <section className="mt-4">
        <h3 className="px-3 py-1 bg-red-800 text-white">HP: {hp}</h3>
      </section>

      {/* Shop */}
      <section className="w-[50%] mx-auto">
        {/* Item 1 */}
        <div className="flex justify-between">
          <div>
            <h3>Item Damage</h3>
            <p>Adds Damage</p>
            <span>
              {damage} ➡️ {damage + 1}
            </span>
          </div>

          <div className="flex flex-col">
            <span>Price: {itemDamagePrice}</span>
            <button
              onClick={itemAddDamage}
              className={`px-4 py-1 rounded mt-auto ${
                coins >= itemDamagePrice ? "bg-amber-400" : "bg-gray-500"
              }`}
            >
              {itemDamageLevel > 0 ? "Upgrade" : "Buy"}
            </button>
          </div>
        </div>

        {/* Item 2 */}
        <div className="flex justify-between">
          <div>
            <h3>Item Auto Clicker</h3>
            <p>Auto Click per Seconds</p>
            <span>
              {autoClickInterval / 1000}s -0.3s
            </span>
          </div>

          <div className="flex flex-col">
            <span>Price: {itemAutoClickPrice}</span>
            <span>Level: {itemAutoClickLevel}</span>
            <button
              onClick={buyAutoClicker}
              className={`px-4 py-1 rounded mt-auto ${
                coins >= itemAutoClickPrice ? "bg-amber-400" : "bg-gray-500"
              }`}
            >
              {itemAutoClickLevel > 0 ? "Upgrade" : "Buy"}
            </button>
          </div>
        </div>
      </section>
    </main>
  );
};

export default Game;
