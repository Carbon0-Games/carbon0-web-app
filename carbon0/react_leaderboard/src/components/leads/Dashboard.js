import React, { Fragment } from "react";
import Leaderboard from "./Leaderboard";
import EveryoneElse from "./EveryoneElse";

export default function Dashboard() {
  return (
    <Fragment>
      <Leaderboard />
      <EveryoneElse />
    </Fragment>
  );
}