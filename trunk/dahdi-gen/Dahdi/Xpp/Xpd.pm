package Dahdi::Xpp::Xpd;
#
# Written by Oron Peled <oron@actcom.co.il>
# Copyright (C) 2007, Xorcom
# This program is free software; you can redistribute and/or
# modify it under the same terms as Perl itself.
#
# $Id: Xpd.pm 6647 2009-05-19 16:46:06Z tzafrir $
#
use strict;
use Dahdi::Utils;
use Dahdi::Xpp;
use Dahdi::Xpp::Line;

my %file_warned;	# Prevent duplicate warnings about same file.

sub xpd_attr_path($@) {
	my $self = shift || die;
	my ($busnum, $unitnum, $subunitnum, @attr) = (
		$self->xbus->num,
		$self->unit,
		$self->subunit,
		@_);
	foreach my $attr (@attr) {
		my $file = sprintf "$Dahdi::Xpp::sysfs_xpds/%02d:%1d:%1d/$attr",
		   $busnum, $unitnum, $subunitnum;
		unless(-f $file) {
			my $procfile = sprintf "/proc/xpp/XBUS-%02d/XPD-%1d%1d/$attr",
			   $busnum, $unitnum, $subunitnum;
			warn "$0: warning - OLD DRIVER: missing '$file'. Fall back to /proc\n"
				unless $file_warned{$attr}++;
			$file = $procfile;
		}
		next unless -f $file;
		return $file;
	}
	return undef;
}

# Backward compat plug for old /proc interface...
sub xpd_old_gettype($) {
	my $xpd = shift || die;
	my $summary = "/proc/xpp/" . $xpd->fqn . "/summary";
	open(F, $summary) or die "Failed to open '$summary': $!";
	my $head = <F>;
	close F;
	chomp $head;
	$head =~ s/^XPD-\d+\s+\(//;
	$head =~ s/,.*//;
	return $head;
}

sub xpd_old_getspan($) {
	my $xpd = shift || die;
	my $dahdi_registration = "/proc/xpp/" . $xpd->fqn . "/dahdi_registration";
	open(F, $dahdi_registration) or die "Failed to open '$dahdi_registration': $!";
	my $head = <F>;
	close F;
	chomp $head;
	return $head;
}

sub xpd_old_getoffhook($) {
	my $xpd = shift || die;
	my $summary = "/proc/xpp/" . $xpd->fqn . "/summary";
	my $channels;

	local $/ = "\n";
	open(F, "$summary") || die "Failed opening $summary: $!\n";
	my $head = <F>;
	chomp $head;	# "XPD-00 (BRI_TE ,card present, span 3)"
	my $offhook;
	while(<F>) {
		chomp;
		if(s/^\s*offhook\s*:\s*//) {
			s/\s*$//;
			$offhook = $_;
			$offhook || die "No channels in '$summary'";
			last;
		}
	}
	close F;
	return $offhook;
}

my %attr_missing_warned;	# Prevent duplicate warnings

sub xpd_driver_getattr($$) {
	my $xpd = shift || die;
	my $attr = shift || die;
	$attr = lc($attr);
	my ($busnum, $unitnum, $subunitnum) = ($xpd->xbus->num, $xpd->unit, $xpd->subunit);
	my $file = sprintf "$Dahdi::Xpp::sysfs_xpds/%02d:%1d:%1d/driver/$attr",
			$busnum, $unitnum, $subunitnum;
	if(!defined($file)) {
		warn "$0: xpd_driver_getattr($attr) -- Missing attribute.\n" if
			$attr_missing_warned{$attr};
		return undef;
	}
	open(F, $file) || return undef;
	my $val = <F>;
	close F;
	chomp $val;
	return $val;
}

sub xpd_getattr($$) {
	my $xpd = shift || die;
	my $attr = shift || die;
	$attr = lc($attr);
	my $file = $xpd->xpd_attr_path(lc($attr));

	# Handle special cases for backward compat
	return xpd_old_gettype($xpd) if $attr eq 'type' and !defined $file;
	return xpd_old_getspan($xpd) if $attr eq 'span' and !defined $file;
	return xpd_old_getoffhook($xpd) if $attr eq 'offhook' and !defined $file;
	if(!defined($file)) {
		warn "$0: xpd_getattr($attr) -- Missing attribute.\n" if
			$attr_missing_warned{$attr};
		return undef;
	}
	open(F, $file) || return undef;
	my $val = <F>;
	close F;
	chomp $val;
	return $val;
}

sub xpd_setattr($$$) {
	my $xpd = shift || die;
	my $attr = shift || die;
	my $val = shift;
	$attr = lc($attr);
	my $file = xpd_attr_path($xpd, $attr);
	my $oldval = $xpd->xpd_getattr($attr);
	open(F, ">$file") or die "Failed to open $file for writing: $!";
	print F "$val";
	if(!close(F)) {
		if($! == 17) {	# EEXISTS
			# good
		} else {
			return undef;
		}
	}
	return $oldval;
}

sub blink($$) {
	my $self = shift;
	my $on = shift;
	my $result = $self->xpd_getattr("blink");
	if(defined($on)) {		# Now change
		$self->xpd_setattr("blink", ($on)?"0xFFFF":"0");
	}
	return $result;
}

sub dahdi_registration($$) {
	my $self = shift;
	my $on = shift;
	my $result;
	my $file = $self->xpd_attr_path("span", "dahdi_registration");
	die "$file is missing" unless -f $file;
	# First query
	open(F, "$file") or die "Failed to open $file for reading: $!";
	$result = <F>;
	chomp $result;
	close F;
	if(defined($on) and $on ne $result) {		# Now change
		open(F, ">$file") or die "Failed to open $file for writing: $!";
		print F ($on)?"1":"0";
		if(!close(F)) {
			if($! == 17) {	# EEXISTS
				# good
			} else {
				undef $result;
			}
		}
	}
	return $result;
}

sub xpds_by_spanno() {
	my @xbuses = Dahdi::Xpp::xbuses();
	my @xpds = map { $_->xpds } @xbuses;
	@xpds = grep { $_->spanno } @xpds;
	@xpds = sort { $a->spanno <=> $b->spanno } @xpds;
	my @spanno = map { $_->spanno } @xpds;
	my @idx;
	@idx[@spanno] = @xpds;	# The spanno is the index now
	return @idx;
}

sub new($$$$$) {
	my $pack = shift or die "Wasn't called as a class method\n";
	my $xbus = shift || die;
	my $unit = shift;	# May be zero
	my $subunit = shift;	# May be zero
	my $procdir = shift || die;
	my $sysfsdir = shift || die;
	my $self = {
		XBUS		=> $xbus,
		ID		=> sprintf("%1d%1d", $unit, $subunit),
		FQN		=> $xbus->name . "/" . "XPD-$unit$subunit",
		UNIT		=> $unit,
		SUBUNIT		=> $subunit,
		DIR		=> $procdir,
		SYSFS_DIR	=> $sysfsdir,
		};
	bless $self, $pack;
	my @offhook = split / /, ($self->xpd_getattr('offhook'));
	$self->{CHANNELS} = @offhook;
	my $type = $self->xpd_getattr('type');
	my $span = $self->xpd_getattr('span');
	$self->{SPANNO} = $span;
	$self->{TYPE} = $type;
	if($type =~ /BRI_(NT|TE)/) {
		$self->{IS_BRI} = 1;
		$self->{TERMTYPE} = $1;
		$self->{DCHAN_HARDHDLC} = $self->xpd_driver_getattr('dchan_hardhdlc');
	}
	$self->{IS_PRI} = ($type =~ /[ETJ]1/);
	$self->{IS_DIGITAL} = ( $self->{IS_BRI} || $self->{IS_PRI} );
	Dahdi::Xpp::Line->create_all($self, $procdir);
	return $self;
}

#------------------------------------
# static xpd related helper functions
#------------------------------------

sub sync_priority_rank($) {
	my $xpd = shift || die;
	# The @rank array is ordered by priority of sync (good to bad)
	my @rank = (
		($xpd->is_pri and defined($xpd->termtype) and $xpd->termtype eq 'TE'),
		($xpd->is_bri and defined($xpd->termtype) and $xpd->termtype eq 'TE'),
		($xpd->is_pri),
		($xpd->type eq 'FXO'),
		($xpd->is_bri),
		($xpd->type eq 'FXS'),
		);
	for(my $i = 0; $i < @rank; $i++) {
		return $i if $rank[$i];
	}
	return @rank + 1;
}

# An XPD sync priority comparator for sort()
sub sync_priority_compare() {
	my $rank_a = sync_priority_rank($a);
	my $rank_b = sync_priority_rank($b);
	#print STDERR "DEBUG: $rank_a (", $a->fqn, ") $rank_b (", $b->fqn, ")\n";
	return $a->fqn cmp $b->fqn if $rank_a == $rank_b;
	return $rank_a <=> $rank_b;
}

# For debugging: show a list of XPD's with relevant sync info.
sub show_xpd_rank(@) {
	print STDERR "XPD's by rank\n";
	foreach my $xpd (@_) {
		my $type = $xpd->type;
		my $rank = sync_priority_rank($xpd);
		if($xpd->is_digital) {
			$type .= " (TERMTYPE " . ($xpd->termtype || "UNKNOWN") . ")";
		}
		printf STDERR "%3d %-15s %s\n", $rank, $xpd->fqn, $type;
	}
}

sub xpds_by_rank(@) {
	my @xpd_prio = sort sync_priority_compare @_;
	#show_xpd_rank(@xpd_prio);
	return @xpd_prio;
}

1;
