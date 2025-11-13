import React, { useEffect, useState } from "react";

const Enemy = () => {
  // logic
  let [level, setLevel] = useState(1);
  let [hp, setHp] = useState(2);
  let [coins, setCoins] = useState(0);
  let [atk, setAtk] = useState(1);
  let [atkPrice, setAtkPrice] = useState(50);

  useEffect(() => {
    if (hp <= 0) {
      setLevel(++level);
      setHp(BaseHP);
      setCoins((coins += 10));
    }
  }, [level, hp]);

  const BaseHP = () => {
    const base = 2;
    return level * base;
  };

  const buyAtk = () => {
    if (coins >= 50) {
      setAtk(++atk);
      setCoins((coins -= 50));
    }
  };

  return (
    <>
      <header className="flex justify-around bg-amber-200">
        <div>Level: {level}</div>
        <div className="size-10 bg-red-500 text-white">HP: {hp}</div>
        <div className="text-2xl">coins: {coins}</div>
      </header>

      <div className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] ">
        <div className="flex flex-col gap-2">
          <button
            className="ring-1 rounded-xl border-black py-3 px-7"
            onClick={() => setLevel(++level)}
          >
            Add Level
          </button>
          <button
            className="bg-amber-500 rounded-xl border-black border-2 py-3 px-7 hover:translate-y-[-3px] transition-all text-white font-bold"
            onClick={() => setHp((hp -= atk))}
          >
            ENEMY
          </button>
        </div>

        <section>
          <div>
            <h3>Damage Upgrade</h3>
            <p>Adds damage per click</p>
            <span>Attack +{atk}</span>
            <span>Price: +{atkPrice}</span>
            <button
              className={`${
                coins >= 50
                  ? "enable bg-amber-500"
                  : "disable bg-black text-white"
              }`}
              onClick={buyAtk}
            >
              Buy
            </button>
          </div>
        </section>
      </div>
    </>
  );
};

export default Enemy;
