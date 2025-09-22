import type { SVGProps } from "react";

const Logo = (props: SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={200}
    height={200}
    viewBox="0 0 200 200"
    {...props}
  >
    <circle cx="100" cy="100" r="90" fill="#4F46E5" />

    <polygon points="80,65 80,135 140,100" fill="white" />

    {/* <text
      x="50%"
      y="180"
      textAnchor="middle"
      fontFamily="Arial, Helvetica, sans-serif"
      fontSize="28"
      fontWeight="bold"
      fill="#111827"
    >
      Recapify
    </text> */}
  </svg>
);

export default Logo;
