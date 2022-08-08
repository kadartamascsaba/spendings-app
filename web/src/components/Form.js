import React, { useState } from "react";
import { InputStyles } from "../styles/InputStyles";
import { SelectStyles } from "../styles/SelectStyles";
import { ErrorMessage, FormStyles } from "../styles/ComponentStyles";

export default function Form({ setSpendings }) {
  const [state, setState] = useState({
    description: "",
    amount: 0,
    currency: "USD",
  });

  const [error, setError] = useState({
    status: false,
    message: {},
  });

  function handleChange(e) {
    const { name, value } = e.target;

    setState({
      ...state,
      [name]: value,
    });
  }

  function handleSubmit(e) {
    e.preventDefault();
    fetch(`http://localhost:5000/spendings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(state),
    })
      .then(async (res) => {
        const body = await res.json();
        return {
          status: res.status,
          body,
        };
      })
      .then((response) => {
        if (response.status === 201) {
          setState({
            description: "",
            amount: 0,
            currency: "USD",
          });
          setSpendings((prevSpendings) => {
            return [...prevSpendings, response.body];
          });
          setError({
            status: false,
            message: {},
          });
        }
        if (response.status === 400) {
          console.log(response.body);
          setError({
            status: true,
            message: response.body,
          });
        }
      })
      .catch((err) => {
        console.error(err);
      });
  }

  return (
    <>
      <FormStyles>
        <InputStyles
          type="text"
          placeholder="description"
          name="description"
          value={state.description}
          onChange={handleChange}
        />
        <InputStyles
          type="number"
          placeholder="amount"
          name="amount"
          value={state.amount}
          onChange={handleChange}
        />
        <SelectStyles
          name="currency"
          value={state.currency}
          onChange={handleChange}
        >
          <option value="HUF">HUF</option>
          <option value="USD">USD</option>
        </SelectStyles>
        <InputStyles onClick={handleSubmit} type="submit" value="Save" />
      </FormStyles>
      {error.status && "description" in error.message && (
        <ErrorMessage>
          {"description: " + error.message["description"]}
        </ErrorMessage>
      )}
      {error.status && "amount" in error.message && (
        <ErrorMessage>{"amount: " + error.message["amount"]}</ErrorMessage>
      )}
    </>
  );
}
