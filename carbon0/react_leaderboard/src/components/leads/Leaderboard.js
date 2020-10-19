import React, { Fragment } from "react";
import TopThreeUsers from "./TopThreeUsers";
import EveryoneElse from "./EveryoneElse";


export default function Leaderboard() {
  return (
    <Fragment>
      <h1 className="leaderboard">Leaderboard</h1>
      <TopThreeUsers />
      <EveryoneElse />
    </Fragment>
  );
}