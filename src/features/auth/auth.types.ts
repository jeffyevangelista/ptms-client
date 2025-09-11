import type { JwtPayload } from "jwt-decode";

export type DecodedToken = JwtPayload & {
  token_type: string;
  exp: number;
  iat: number;
  jti: string;
  user_id: string;
  user: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    roles: string[];
  };
  business_unit: {
    ids: number[];
    names: string[];
  };
};

export type AuthCredentials = {
  email: string;
  password: string;
};

export type UserType = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  roles: string[];
  business_unit: null | string[];
};
