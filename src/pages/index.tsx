import { Redirect } from "@docusaurus/router";
import useBaseUrl from "@docusaurus/useBaseUrl";

export default function Home() {
  // 用 useBaseUrl 拼出目标地址，部署到 GitHub Pages 这类子路径站点时才不会跳出 baseUrl。
  return <Redirect to={useBaseUrl("/docs/welcome")} />;
}
