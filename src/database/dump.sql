--
-- PostgreSQL database dump
--

\restrict U4Vg6dA0qWlAvSaRpXCm5pgt8z4JJzaOPt6ODtbwXrRdhyCrwvvwDXwuU5qtHQW

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.author (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    surname character varying(100) NOT NULL
);


ALTER TABLE public.author OWNER TO postgres;

--
-- Name: author_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.author_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.author_id_seq OWNER TO postgres;

--
-- Name: author_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.author_id_seq OWNED BY public.author.id;


--
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    pages integer
);


ALTER TABLE public.book OWNER TO postgres;

--
-- Name: book_author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_author (
    book integer NOT NULL,
    author integer NOT NULL
);


ALTER TABLE public.book_author OWNER TO postgres;

--
-- Name: book_genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_genre (
    book integer NOT NULL,
    genre integer NOT NULL
);


ALTER TABLE public.book_genre OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_id_seq OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_id_seq OWNED BY public.book.id;


--
-- Name: book_library; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_library (
    book integer NOT NULL,
    library integer NOT NULL,
    available boolean DEFAULT true,
    link character varying(255)
);


ALTER TABLE public.book_library OWNER TO postgres;

--
-- Name: book_shop; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_shop (
    book integer NOT NULL,
    shop integer NOT NULL,
    price numeric(10,2) NOT NULL,
    link character varying(255)
);


ALTER TABLE public.book_shop OWNER TO postgres;

--
-- Name: favorites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favorites (
    user_id integer NOT NULL,
    book_id integer NOT NULL,
    added_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.favorites OWNER TO postgres;

--
-- Name: genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.genre (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.genre OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genre_id_seq OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.genre_id_seq OWNED BY public.genre.id;


--
-- Name: libraries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.libraries (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address character varying(255)
);


ALTER TABLE public.libraries OWNER TO postgres;

--
-- Name: libraries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.libraries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.libraries_id_seq OWNER TO postgres;

--
-- Name: libraries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.libraries_id_seq OWNED BY public.libraries.id;


--
-- Name: library_specialty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library_specialty (
    library integer NOT NULL,
    specialty integer NOT NULL
);


ALTER TABLE public.library_specialty OWNER TO postgres;

--
-- Name: shop_specialty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_specialty (
    shop integer NOT NULL,
    specialty integer NOT NULL
);


ALTER TABLE public.shop_specialty OWNER TO postgres;

--
-- Name: shops; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shops (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address character varying(255)
);


ALTER TABLE public.shops OWNER TO postgres;

--
-- Name: shops_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shops_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shops_id_seq OWNER TO postgres;

--
-- Name: shops_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shops_id_seq OWNED BY public.shops.id;


--
-- Name: specialty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.specialty (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.specialty OWNER TO postgres;

--
-- Name: specialty_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.specialty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.specialty_id_seq OWNER TO postgres;

--
-- Name: specialty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.specialty_id_seq OWNED BY public.specialty.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    is_admin boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: author id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author ALTER COLUMN id SET DEFAULT nextval('public.author_id_seq'::regclass);


--
-- Name: book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN id SET DEFAULT nextval('public.book_id_seq'::regclass);


--
-- Name: genre id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre ALTER COLUMN id SET DEFAULT nextval('public.genre_id_seq'::regclass);


--
-- Name: libraries id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.libraries ALTER COLUMN id SET DEFAULT nextval('public.libraries_id_seq'::regclass);


--
-- Name: shops id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shops ALTER COLUMN id SET DEFAULT nextval('public.shops_id_seq'::regclass);


--
-- Name: specialty id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialty ALTER COLUMN id SET DEFAULT nextval('public.specialty_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.author (id, name, surname) FROM stdin;
1	Stephen	Hawking
2	Richard	Feynman
3	Charles	Darwin
4	Donald	Knuth
5	Carl	Sagan
6	Albert	Einstein
7	Ada	Lovelace
8	Michio	Kaku
9	James	Watson
10	Alan	Turing
11	Robert	Martin
12	Bjarne	Stroustrup
\.


--
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book (id, name, pages) FROM stdin;
1	A Brief History of Time	256
2	The Feynman Lectures on Physics	1552
3	On the Origin of Species	502
4	The Art of Computer Programming, Vol 1	672
5	Cosmos	365
6	Relativity: The Special and General Theory	168
7	Clean Code	464
8	Physics of the Impossible	329
9	The Double Helix	226
10	Computing Machinery and Intelligence	30
11	The C++ Programming Language	1376
12	Introduction to Algorithms	1312
\.


--
-- Data for Name: book_author; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_author (book, author) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	11
8	8
9	9
10	10
11	12
12	11
\.


--
-- Data for Name: book_genre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_genre (book, genre) FROM stdin;
1	1
1	5
2	1
3	3
4	2
4	4
5	5
6	1
7	2
8	1
9	3
10	2
10	7
11	2
12	2
12	4
\.


--
-- Data for Name: book_library; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_library (book, library, available, link) FROM stdin;
1	1	t	\N
2	1	f	\N
6	1	t	\N
12	1	t	\N
4	2	t	\N
7	2	t	https://uni-lib.edu/download/clean-code.pdf
10	2	t	https://uni-lib.edu/papers/turing.pdf
11	2	f	\N
3	3	t	https://gutenberg.org/ebooks/1228
5	3	t	https://archive.org/details/cosmos
6	3	t	https://gutenberg.org/ebooks/666
1	4	t	\N
5	4	t	\N
8	4	f	\N
\.


--
-- Data for Name: book_shop; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book_shop (book, shop, price, link) FROM stdin;
1	1	15.99	https://amazon.com/brief-history
2	1	120.50	https://amazon.com/feynman-lectures
4	1	55.00	https://amazon.com/knuth-vol1
7	1	40.00	https://amazon.com/clean-code
12	1	85.00	https://amazon.com/algorithms
1	2	450.00	\N
3	2	320.00	\N
6	2	210.00	\N
8	2	380.00	\N
4	3	45.00	https://oreilly.com/knuth
7	3	35.00	https://oreilly.com/clean-code
10	3	10.00	https://oreilly.com/turing-paper
11	3	60.00	https://oreilly.com/cpp
3	4	1500.00	\N
6	4	800.00	\N
\.


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.favorites (user_id, book_id, added_at) FROM stdin;
1	2	2025-12-14 01:24:45.707863
1	3	2025-12-14 01:24:45.707863
\.


--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.genre (id, name) FROM stdin;
1	Physics
2	Computer Science
3	Biology
4	Mathematics
5	Astronomy
6	Chemistry
7	Philosophy of Science
\.


--
-- Data for Name: libraries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.libraries (id, name, address) FROM stdin;
1	Central Science Library	Main Street 101
2	University Tech Archive	Campus Bld 5
3	Online Open Access Lib	Internet
4	City Public Library	Square Ave 12
\.


--
-- Data for Name: library_specialty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.library_specialty (library, specialty) FROM stdin;
1	1
2	5
3	3
4	2
\.


--
-- Data for Name: shop_specialty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shop_specialty (shop, specialty) FROM stdin;
1	2
2	1
3	3
4	4
\.


--
-- Data for Name: shops; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shops (id, name, address) FROM stdin;
1	Amazon Books	Online Global
2	Naukova Dumka	Kyiv, Hrushevskoho 4
3	O'Reilly Media Store	Online
4	Old Book Corner	Lviv, Market Square 1
\.


--
-- Data for Name: specialty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.specialty (id, name) FROM stdin;
1	Academic Literature
2	Popular Science
3	Digital Archives
4	Rare Books
5	University Textbooks
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, is_admin) FROM stdin;
1	user1	user1@gmail.com	scrypt:32768:8:1$CkhpdrBwtpDtAUY9$519d84bc6b6c37634757ee12a4f732ad6d6f0d604b3bb9995b18920e2d4ffc3ab9b5dd30af931fb9ed90317dfa7291ecf15a8d6b22947dd69de59d0e08ce819d	t
9	user6	user6@gmail.com	scrypt:32768:8:1$Izm658EU8Wt4dhHl$d6daf06757ae3ab3055e28d32c572edd451dfcbd0eb567221d0c909a80c5dd89762bdbda9d5334a947dacb3f76c92c4e5aee5e71cca26a82d2a32a33871b4158	f
\.


--
-- Name: author_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.author_id_seq', 14, true);


--
-- Name: book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_id_seq', 15, true);


--
-- Name: genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.genre_id_seq', 7, true);


--
-- Name: libraries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.libraries_id_seq', 4, true);


--
-- Name: shops_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shops_id_seq', 4, true);


--
-- Name: specialty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.specialty_id_seq', 5, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 9, true);


--
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (id);


--
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);


--
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (user_id, book_id);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: libraries libraries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.libraries
    ADD CONSTRAINT libraries_pkey PRIMARY KEY (id);


--
-- Name: book_author pk_book_author; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT pk_book_author PRIMARY KEY (book, author);


--
-- Name: book_genre pk_book_genre; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT pk_book_genre PRIMARY KEY (book, genre);


--
-- Name: book_library pk_book_library; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_library
    ADD CONSTRAINT pk_book_library PRIMARY KEY (book, library);


--
-- Name: book_shop pk_book_shop; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_shop
    ADD CONSTRAINT pk_book_shop PRIMARY KEY (book, shop);


--
-- Name: library_specialty pk_library_specialty; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_specialty
    ADD CONSTRAINT pk_library_specialty PRIMARY KEY (library, specialty);


--
-- Name: shop_specialty pk_shop_specialty; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_specialty
    ADD CONSTRAINT pk_shop_specialty PRIMARY KEY (shop, specialty);


--
-- Name: shops shops_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_pkey PRIMARY KEY (id);


--
-- Name: specialty specialty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialty
    ADD CONSTRAINT specialty_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: favorites favorites_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(id) ON DELETE CASCADE;


--
-- Name: favorites favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: book_author fk_ba_author; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT fk_ba_author FOREIGN KEY (author) REFERENCES public.author(id) ON DELETE CASCADE;


--
-- Name: book_author fk_ba_book; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT fk_ba_book FOREIGN KEY (book) REFERENCES public.book(id) ON DELETE CASCADE;


--
-- Name: book_genre fk_bg_book; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT fk_bg_book FOREIGN KEY (book) REFERENCES public.book(id) ON DELETE CASCADE;


--
-- Name: book_genre fk_bg_genre; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT fk_bg_genre FOREIGN KEY (genre) REFERENCES public.genre(id) ON DELETE CASCADE;


--
-- Name: book_library fk_bl_book; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_library
    ADD CONSTRAINT fk_bl_book FOREIGN KEY (book) REFERENCES public.book(id) ON DELETE CASCADE;


--
-- Name: book_library fk_bl_library; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_library
    ADD CONSTRAINT fk_bl_library FOREIGN KEY (library) REFERENCES public.libraries(id) ON DELETE CASCADE;


--
-- Name: book_shop fk_bs_book; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_shop
    ADD CONSTRAINT fk_bs_book FOREIGN KEY (book) REFERENCES public.book(id) ON DELETE CASCADE;


--
-- Name: book_shop fk_bs_shop; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_shop
    ADD CONSTRAINT fk_bs_shop FOREIGN KEY (shop) REFERENCES public.shops(id) ON DELETE CASCADE;


--
-- Name: library_specialty fk_ls_library; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_specialty
    ADD CONSTRAINT fk_ls_library FOREIGN KEY (library) REFERENCES public.libraries(id) ON DELETE CASCADE;


--
-- Name: library_specialty fk_ls_specialty; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_specialty
    ADD CONSTRAINT fk_ls_specialty FOREIGN KEY (specialty) REFERENCES public.specialty(id) ON DELETE CASCADE;


--
-- Name: shop_specialty fk_ss_shop; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_specialty
    ADD CONSTRAINT fk_ss_shop FOREIGN KEY (shop) REFERENCES public.shops(id) ON DELETE CASCADE;


--
-- Name: shop_specialty fk_ss_specialty; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_specialty
    ADD CONSTRAINT fk_ss_specialty FOREIGN KEY (specialty) REFERENCES public.specialty(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict U4Vg6dA0qWlAvSaRpXCm5pgt8z4JJzaOPt6ODtbwXrRdhyCrwvvwDXwuU5qtHQW

