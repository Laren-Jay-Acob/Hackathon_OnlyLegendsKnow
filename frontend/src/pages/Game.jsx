import React, { useEffect, useState } from "react";

const Game = () => {
  // Logic
  const [level, setLevel] = useState(1);
  const [hp, setHp] = useState(2);
  const [coins, setCoins] = useState(0);
  const [damage, setDamage] = useState(1);
  const [itemDamageLevel, setItemDamageLevel] = useState(0);
  const [itemDamagePrice, setItemDamagePrice] = useState(50);
  const [itemAutoClickLevel, setItemAutoClickLevel] = useState(0);
  const [autoClickInterval, setAutoClickInterval] = useState(3300);
  const [itemAutoClickPrice, setItemAutoClickPrice] = useState(50);

  const BaseHP = () => level * 2;

  // fetch on mount
  useEffect(() => {
    const fetchOnMount = async () => {
      const res = await fetch("http://127.0.0.1:5000/all/get");
      const data = await res.json();

      setCoins(data.msg.coins.amount);
      setLevel(data.msg.player.level);
      setItemDamageLevel(data.msg.items[1].item_level);
      setItemAutoClickLevel(data.msg.items[0].item_level);

      setItemDamagePrice(data.msg.items[1].item_price);
      setItemAutoClickPrice(data.msg.items[0].item_price);
    };

    fetchOnMount();
  }, []);

  const dataCoinLevelUp = async () => {
    const resCoin = await fetch("http://127.0.0.1:5000/coins/gain", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ coins: 10 }),
    });
    const dataCoin = resCoin.json();
    console.log(dataCoin);

    const res = await fetch("http://127.0.0.1:5000/player/level_up");
    const data = res.json();
    console.log(data);
  };

  useEffect(() => {
    if (hp <= 0) {
      setLevel((prev) => prev + 1);
      setHp(BaseHP);
      setCoins((prev) => prev + 10);
      const data_in_func = dataCoinLevelUp();
      console.log(data_in_func);
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
  const itemAddDamage = async () => {
    if (coins >= itemDamagePrice) {
      setCoins((prev) => prev - itemDamagePrice);
      setDamage((d) => d + 1);
      setItemDamagePrice((prev) => Math.floor(prev * 1.5));

      const res = await fetch("http://127.0.0.1:5000/shop/item_level", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: 2 }),
      });
      const data = res.json();
      console.log(data);

      const resprice = await fetch("http://127.0.0.1:5000/shop/item/price", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: 2,
          price: itemDamagePrice,
        }),
      });
      const dataprice = resprice.json();
      console.log(dataprice);
    }
  };

  // item Auto Clicker
  const buyAutoClicker = async () => {
    if (coins >= itemAutoClickPrice) {
      console.log("Buy Auto Clicker...");
      setCoins((prev) => prev - itemAutoClickPrice);
      setItemAutoClickLevel((prev) => prev + 1);
      setItemAutoClickPrice((prev) => Math.floor(prev * 1.5));
      console.log(itemAutoClickPrice);

      if (autoClickInterval > 0.75) {
        setAutoClickInterval((prev) => prev - 300);

        const res = await fetch("http://127.0.0.1:5000/shop/item_level", {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: 1 }),
        });
        const data = res.json();
        console.log(data);

        const resprice = await fetch("http://127.0.0.1:5000/shop/item/price", {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id: 1,
            price: itemAutoClickPrice,
          }),
        });
        const dataprice = resprice.json();
        console.log(itemAutoClickPrice);
        console.log(dataprice);
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
            <span>{autoClickInterval / 1000}s -0.3s</span>
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
