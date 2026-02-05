-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 05, 2026 at 01:06 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inlamning_1`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(300) NOT NULL,
  `name` varchar(250) NOT NULL,
  `email` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `name`, `email`) VALUES
(8, '1', 'scrypt:32768:8:1$YE6gzERmwTiTiz8C$90cffe6f7846af8c0d6c8fc9ea5a8f17170c83eb49d9972760327d54a8cba822f9e65c451e7b90524befbe49baf6d0188904dfbef14bd88ef44097e5135284c8', '1', 'test@example.com'),
(9, '2', 'scrypt:32768:8:1$bEcp0GxssdqOIuxt$24467810a83d53e817ad2305ec9eea944d0045ba2cbbb59b0d28b96d4675ee38dfd5c9c5df839413b312eeb3a49563791a0e88f5ea0b89b00bd31980e25e1f22', '2', '2test@example.com'),
(11, 'username_test', 'scrypt:32768:8:1$UQXIsmaBxRN2K43h$e6c4d3b385226bfc03f4dd080230e375e06592263660f82f1f36e09d19fa6d44e5e7002ad23b325f2199fc8a86d2ea8054f431a7022edb9dd9dccfb9a3cff46b', 'name_test', ''),
(12, 'username_test1', 'scrypt:32768:8:1$zMxvIwdvgXexZ5yE$3a820e87c30a921a3af9b214923813dab87754f0769a03ad7a040137534a9d5930d6210d70fd444ab774cc7d4c9ebdfd06f122a9416bff0127c658a641a9525a', 'name_test1', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username_unique` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
