import { Outlet, NavLink, Link } from "react-router-dom";
import github from "../../assets/github.svg";
import sunnythebotIcon from "../../assets/sunnythebot-icon.svg";
import styles from "./Layout.module.css";
import { useLogin } from "../../authConfig";
import { LoginButton } from "../../components/LoginButton";

const Layout = () => {
    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Link to="/" className={styles.headerTitleContainer}>
                        <img src={sunnythebotIcon} alt="SunnyTheBot Icon" className={styles.headerLogo} />
                        <h3 className={styles.headerTitle}>SunnyTheBot</h3>
                    </Link>
                    <div className={styles.headerRight}>
                        <nav>
                            <ul className={styles.headerNavList}>
                                <li>
                                    <NavLink to="/" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                                        Chat
                                    </NavLink>
                                </li>
                                <li className={styles.headerNavLeftMargin}>
                                    <NavLink to="/qa" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                                        Ask a question
                                    </NavLink>
                                </li>
                            </ul>
                        </nav>
                        <a href="https://aka.ms/entgptsearch" target={"_blank"} title="Github repository link" className={styles.githubLink}>
                            <img
                                src={github}
                                alt="Github logo"
                                aria-label="Link to github repository"
                                width="20px"
                                height="20px"
                                className={styles.githubLogo}
                            />
                        </a>
                    </div>
                    {useLogin && <LoginButton />}
                </div>
            </header>

            <Outlet />
        </div>
    );
};

export default Layout;
