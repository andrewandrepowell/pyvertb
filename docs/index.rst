.. pyvertb documentation master file, created by
   sphinx-quickstart on Tue May  4 09:40:28 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========
Overview
========

This sections includes a conceptual overview of the components of a pyvertb testbench;
high-level guidelines on how to write pyvertb testbenches;
and references to interesting helpers and implementation bits.

Each section will start out more conceptual and will get more specific in each section.
If you wish to only get a conceptual understanding or judge pyvertb's capabilities,
read until it get too detailed, skip the rest of the section, and maybe look at the code samples.


Processes, Modules, and Communication
=====================================

Testbenches in pyvertb are comprised of :class:`Component`\ s, which are any structural element of a testbench.
There are two main categories of Components:
:class:`Process`\ es, which are independent subprograms doing work simultaneous to other Processes;
and :class:`Module`\ s, which are structural collections of Processes or other Modules.
Processes communicate with other Processes not by sharing state,
but by passing data over :class:`Channel`\ s.

This parallels many HDLs or simulation frameworks.
In terms of Verilog, you can think of Processes as ``always`` blocks,
Modules as Verilog ``module``\ s,
and Channels as ``wire``\ s.
Or in terms of VHDL, you can think of Processes as VHDL ``process`` statements,
Modules as ``entity``\ s,
and Channels as ``signal``\ s.

Channels, Sources and Sinks
---------------------------

* Processes *pull* data from Sources
* Processes *put* data in Sinks
* Channels bridge on Processes output to another's input by acting as both a Sink and a Source
* Other kinds of Sources:
    * (Infinite) iterators
* Other kinds of Sinks:
    * NullSink
    * Collections (list, set)

Transactions
============

pyvertb's :class:`Process`\ es, :class:`Module`\ s, and :class:`Channel`\ s are agnostic to the types of data they operate on.
This can be useful

Reusable HDL Interfaces
=======================

Interfaces
----------

* Define a consistent Python representation of an HDL interface
* Includes:
    * Simulator Object Handles
    * Configurations

Drivers and Monitors
--------------------

* Driver
    * Maps specific Transaction types to specific Interface types
    * Can send a request and get a response
* Monitor
    * Passively observes Transactions occuring on Interface

Synchronous
~~~~~~~~~~~

* Uses blocking coroutines

Asynchronous
~~~~~~~~~~~~

* Uses Channels

Ad-hoc Drivers and Monitors
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Testing
=======

* Functional Correctness and Coverage
* Deciding stimulus
* Deciding test end

Modeling
--------

* Use numpy, MATLAB, C++ + pybind11, etc.
* Wrap as a Process, or use ad-hoc process

Scorers and Scoreboards
-----------------------

* Scorers have single responsibility
    * Coverage bins
    * Matching actuals/expecteds
    * Assertions
* Scoreboards manage Scorers and aggregate data

Best Practices
--------------

* Use *observed* inputs, do not pass stimulus to matcher
* Don't assume 1-to-1 input-to-output correspondence, even if expected
* Analyze coverage complexity (can you test for 100% coverage befor the heat death of the universe?)

Dividing Testbenching Responsibility
====================================

Structuring For Reuse
---------------------

* Active components are usually only reusable at the top level
* Passive components can be reused anywhere

Analyzers
---------

* Reusable Modules with:
    * Passive components
    * Models
    * Assertions
    * Scorers

Reusable per entity instantiation.
Design for possibility of multiple instances if possible.

Stimulators
-----------

* Reusable Modules with:
    * Active components
    * Drivers

Reusable per top.
