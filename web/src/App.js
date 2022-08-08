import React, { useState } from "react";
import Form from "./components/Form";
import FiltersAndOrderings from "./components/FiltersAndOrderings";
import SpendingList from "./components/SpendingList";
import Layout from "./components/Layout";

export default function App() {
  const [spendings, setSpendings] = useState([]);
  const [filtering, setFiltering] = useState("ALL");
  const [ordering, setOrdering] = useState("-spent_at");

  return (
    <>
      <Layout>
        <Form setSpendings={setSpendings} />
        <FiltersAndOrderings
          setFiltering={setFiltering}
          filtering={filtering}
          setOrdering={setOrdering}
        />
        <SpendingList
          spendings={spendings}
          ordering={ordering}
          filtering={filtering}
          setSpendings={setSpendings}
        />
      </Layout>
    </>
  );
}
