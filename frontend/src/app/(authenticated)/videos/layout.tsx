import { SiteHeader } from "@/components/site-header";

import { Fragment, PropsWithChildren } from "react";

export default function Layout({ children }: PropsWithChildren) {
  return (
    <Fragment>
      <SiteHeader title="Videos" />
      <div className="flex flex-1 flex-col">
        <div className="@container/main flex flex-1 flex-col gap-2">
          {children}
        </div>
      </div>
    </Fragment>
  );
}
