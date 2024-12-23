-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 23, 2024 at 01:46 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `reckomov`
--

-- --------------------------------------------------------

--
-- Table structure for table `akun_user`
--

CREATE TABLE `akun_user` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `id_data` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `akun_user`
--

INSERT INTO `akun_user` (`email`, `password`, `username`, `id_data`) VALUES
('amir@gmail.com', '1234', 'contoh', 'amicon'),
('amiruddinstr@gmail.com', '11223344', 'contoh', 'ami112'),
('bella@gmail.com', '12345678', 'belladian', 'belbel'),
('contoh@gmail.com', 'contoh123', 'contoh', 'concon'),
('nanang@gmail.com', '1234', 'anang', 'nanana'),
('sitor@gmail.com', '1234', 'sitor', 'sitsit'),
('toba@gmail.com', '11223333', 'toba amiruddin', 'tobaa'),
('udin@gmail.com', '1234', 'udin', 'udiudi');

-- --------------------------------------------------------

--
-- Table structure for table `data_film_user`
--

CREATE TABLE `data_film_user` (
  `id_data` varchar(50) NOT NULL,
  `bookmark_film` varchar(999) DEFAULT NULL,
  `favorit_film` varchar(999) DEFAULT NULL,
  `preferensi` varchar(999) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_film_user`
--

INSERT INTO `data_film_user` (`id_data`, `bookmark_film`, `favorit_film`, `preferensi`) VALUES
('ami112', '[]', '[]', '[]'),
('amicon', '[]', '[1114513]', '[]'),
('belbel', '[]', '[]', '[]'),
('concon', '[1005331]', '[1005331]', '[]'),
('nanana', '[1034541]', '[]', '[16]'),
('sitsit', '[]', '[]', '[]'),
('tobaa', '[1035048]', '[19404, 1035048]', '[]'),
('udiudi', '[]', '[]', '[28, 37, 10752, 878]');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `akun_user`
--
ALTER TABLE `akun_user`
  ADD PRIMARY KEY (`email`),
  ADD KEY `fk_id_data` (`id_data`);

--
-- Indexes for table `data_film_user`
--
ALTER TABLE `data_film_user`
  ADD PRIMARY KEY (`id_data`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `akun_user`
--
ALTER TABLE `akun_user`
  ADD CONSTRAINT `fk_id_data` FOREIGN KEY (`id_data`) REFERENCES `data_film_user` (`id_data`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
