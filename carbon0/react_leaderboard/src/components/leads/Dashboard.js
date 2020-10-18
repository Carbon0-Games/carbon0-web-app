import React, { Fragment } from "react";
import TopThreeUser from "./TopThreeUser";
import EveryoneElse from "./EveryoneElse";

export default function Dashboard() {
  return (
    <Fragment>
      <h1 className="leaderboard">Leaderboard</h1>
      <TopThreeUser />
      <EveryoneElse />
    </Fragment>
  );
}