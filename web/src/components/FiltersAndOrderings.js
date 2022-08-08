import React from "react";

import {
  FiltersWrapper,
  Orderings,
  CurrencyFilters,
  CurrencyButton,
} from "../styles/ComponentStyles";

export default function CurrencyFilter({
  setFiltering,
  filtering,
  setOrdering,
}) {
  function handleClick(e) {
    setFiltering(e.target.name);
  }

  return (
    <>
      <FiltersWrapper>
        <Orderings>
          <select onChange={(e) => setOrdering(e.target.value)}>
            <option value="-spent_at">Sort by Date descending (default)</option>
            <option value="spent_at">Sort by Date ascending</option>
            <option value="-amount">Sort by Amount descending</option>
            <option value="amount">Sort by Amount ascending</option>
          </select>
        </Orderings>
        <CurrencyFilters>
          <li onClick={handleClick}>
            <CurrencyButton currencyFilter={filtering} name="ALL">
              ALL
            </CurrencyButton>
          </li>
          <li onClick={handleClick}>
            <CurrencyButton currencyFilter={filtering} name="HUF">
              HUF
            </CurrencyButton>
          </li>
          <li onClick={handleClick}>
            <CurrencyButton currencyFilter={filtering} name="USD">
              USD
            </CurrencyButton>
          </li>
        </CurrencyFilters>
      </FiltersWrapper>
    </>
  );
}
