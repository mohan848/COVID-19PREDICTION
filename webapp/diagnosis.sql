-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2021 at 06:57 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `diagnosis`
--

-- --------------------------------------------------------

--
-- Table structure for table `employee_details`
--

CREATE TABLE `employee_details` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employee_details`
--

INSERT INTO `employee_details` (`username`, `password`) VALUES
('mohan', 'mohan'),
('nivas', 'nivas');

-- --------------------------------------------------------

--
-- Table structure for table `test_results`
--

CREATE TABLE `test_results` (
  `ID` int(11) NOT NULL,
  `result` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `test_results`
--

INSERT INTO `test_results` (`ID`, `result`) VALUES
(5, 'Pneumonia'),
(10, 'Covid19 Positive'),
(13, 'Normal'),
(11, 'Pneumonia'),
(22, 'Normal'),
(18, 'Pneumonia'),
(17, 'Covid19 Positive'),
(19, 'Pneumonia'),
(20, 'Covid19 Positive'),
(15, 'Covid19 Positive'),
(14, 'Normal');

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `ID` int(11) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `age` int(11) NOT NULL,
  `mobile_num` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'Y'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_details`
--

INSERT INTO `user_details` (`ID`, `email`, `name`, `gender`, `age`, `mobile_num`, `password`, `status`) VALUES
(5, 'mohan@gmail.com', 'Mohan', 'Male', 20, '6379462299', 'mohan', 'D'),
(10, 'anil@gmail.com', 'anil', 'Male', 45, '9392484888', 'G3WH56SH', 'D'),
(11, 'uma@gmail.com', 'uma', 'Female', 38, '8074976655', 'JA9MBQ1J', 'D'),
(13, 'rama@gmail.com', 'rama', 'Female', 45, '9090909090', '2QD2ZG4M', 'D'),
(14, 'tarun@gmail.com', 'tarun', 'Male', 20, '9090212121', '2I8I34YT', 'D'),
(15, 'kiran@gmail.com', 'kiran', 'Male', 56, '8909889878', 'CID469CP', 'D'),
(16, 'laks@gmail.com', 'lakshmi', 'Female', 28, '7865669871', 'PV4YUFKZ', 'Y'),
(17, 'charan@gmail.com', 'charan', 'Male', 34, '9089898832', 'GC35C1UZ', 'D'),
(18, 'geetha@gmail.com', 'geetha', 'Female', 19, '8876766761', 'ZVI0FG23', 'D'),
(19, 'lavn@gmail.com', 'lavanya', 'Female', 25, '9087878798', 'SMXXDBZ9', 'D'),
(20, 'kar@gmail.com', 'karthik', 'Male', 67, '9888007123', 'RS4BWFFQ', 'D'),
(21, '', 'harsha', 'Male', 39, '6789321456', 'J6GE8CEX', 'Y'),
(22, 'vamsi@gmail.com', 'vamsi', 'Male', 21, '7689452310', 'SG05TPON', 'D');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user_details`
--
ALTER TABLE `user_details`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user_details`
--
ALTER TABLE `user_details`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
