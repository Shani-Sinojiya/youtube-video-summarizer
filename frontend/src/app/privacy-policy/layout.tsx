import { Metadata } from "next/types";
import React, { Fragment, PropsWithChildren } from "react";

const Layout = ({ children }: PropsWithChildren) => {
  return <Fragment>{children}</Fragment>;
};

export default Layout;

export const metadata: Metadata = {
  title: "Recapify - Privacy Policy",
  description:
    "Learn how Recapify protects your privacy and handles your data.",
};
